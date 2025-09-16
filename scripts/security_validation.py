#!/usr/bin/env python3
# =============================================================================
# AI对话系统安全扫描验证脚本
# 核心校验逻辑：主问题存在性、分支检查、检查点验证、文档合规性、更新验证
# =============================================================================

import sys
import os
import requests
from typing import Dict, List, Tuple, Optional

# -----------------------------
# 1) 配置参数（宽松版本）
# -----------------------------
CONFIG = {
    # GitHub环境配置
    "GITHUB_ENV": {
        "ORGANIZATION": "your-organization",  # 替换为实际组织名
        "REPOSITORY": "ai-chatbot-security-scanner",  # 替换为实际仓库名
        "TOKEN_ENV_VAR": "GITHUB_TOKEN",
    },

    # 主安全问题配置
    "MAIN_ISSUE": {
        "TITLE": "安全漏洞扫描：对话系统风险检测",
        "EXACT_TITLE_MATCH": False,  # 宽松匹配，允许包含关键词
        "REQUIRED_LABELS": ["安全", "漏洞", "AI对话", "风险检测"],
        "REQUIRE_ALL_LABELS": False,  # 只需要包含部分标签
    },

    # 安全检查分支配置
    "BRANCHES": {
        "REQUIRED_BRANCHES": [
            "security-scan",
            "privacy-check", 
            "api-audit"
        ],
        "MIN_BRANCHES": 2,  # 至少需要2个分支
    },

    # 安全检查点配置
    "CHECKPOINTS": {
        "EXPECTED_KEYWORDS": [
            "用户输入处理",
            "对话响应",
            "权限验证",
            "API接口"
        ],
        "MIN_CHECKPOINTS": 3,  # 至少需要3个检查点
    },

    # 评论配置
    "COMMENTS": {
        "MIN_COMMENTS": 2,  # 至少需要2条评论
        "REQUIRED_KEYWORDS": [
            "src/utils/security.py",
            "src/api/auth.py", 
            "config/settings.py"
        ],
    },

    # 安全更新配置
    "SECURITY_UPDATE": {
        "REQUIRED": True,
        "TITLE": "安全更新：基础漏洞修复",
        "EXACT_TITLE_MATCH": False,
        "SOURCE_BRANCH": "security-scan",
    }
}

# -----------------------------
# 2) 工具函数
# -----------------------------

def _get_github_headers() -> Dict[str, str]:
    """获取GitHub API请求头"""
    token = os.getenv(CONFIG["GITHUB_ENV"]["TOKEN_ENV_VAR"])
    if not token:
        print(f"[WARNING] 环境变量 {CONFIG['GITHUB_ENV']['TOKEN_ENV_VAR']} 未设置，使用无认证访问")
        return {"Accept": "application/vnd.github.v3+json"}
    
    return {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
    }

def _call_github_api(endpoint: str, headers: Dict[str, str]) -> Tuple[bool, Optional[List[Dict]]]:
    """调用GitHub API"""
    base_url = f"https://api.github.com/repos/{CONFIG['GITHUB_ENV']['ORGANIZATION']}/" \
               f"{CONFIG['GITHUB_ENV']['REPOSITORY']}"
    url = f"{base_url}/{endpoint}"
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            data = response.json()
            return True, data if isinstance(data, list) else [data]
        else:
            print(f"[WARNING] API访问可能受限 ({endpoint}): {response.status_code}")
            return False, None
    except Exception as e:
        print(f"[WARNING] API请求异常 ({endpoint}): {str(e)}")
        return False, None

def _validate_main_issue(headers: Dict[str, str]) -> Tuple[bool, Optional[int]]:
    """验证主安全问题"""
    success, issues = _call_github_api("issues?state=open&per_page=50", headers)
    if not success:
        return False, None

    for issue in issues or []:
        title = issue.get("title", "")
        
        # 宽松标题匹配
        if CONFIG["MAIN_ISSUE"]["EXACT_TITLE_MATCH"]:
            title_match = (title == CONFIG["MAIN_ISSUE"]["TITLE"])
        else:
            title_match = any(keyword in title for keyword in ["安全", "漏洞", "扫描"])
        
        if not title_match:
            continue

        # 宽松标签匹配
        issue_labels = {label.get("name", "") for label in issue.get("labels", [])}
        required_labels = set(CONFIG["MAIN_ISSUE"]["REQUIRED_LABELS"])
        
        if CONFIG["MAIN_ISSUE"]["REQUIRE_ALL_LABELS"]:
            label_match = required_labels.issubset(issue_labels)
        else:
            label_match = len(required_labels.intersection(issue_labels)) >= 2  # 至少2个匹配标签

        if label_match:
            return True, issue.get("number")

    return False, None

def _validate_branches(headers: Dict[str, str]) -> bool:
    """验证安全检查分支"""
    success, branches = _call_github_api("branches?per_page=50", headers)
    if not success:
        return False

    existing_branches = {branch.get("name", "") for branch in branches or []}
    required_branches = set(CONFIG["BRANCHES"]["REQUIRED_BRANCHES"])
    
    found_branches = required_branches.intersection(existing_branches)
    if len(found_branches) >= CONFIG["BRANCHES"]["MIN_BRANCHES"]:
        print(f"[OK] 找到 {len(found_branches)} 个安全检查分支: {', '.join(found_branches)}")
        return True
    else:
        print(f"[WARNING] 安全检查分支不足: 需要{CONFIG['BRANCHES']['MIN_BRANCHES']}个，找到{len(found_branches)}个")
        return False

def _validate_checkpoints(main_issue_number: int, headers: Dict[str, str]) -> bool:
    """验证安全检查点"""
    success, all_issues = _call_github_api("issues?state=open&per_page=50", headers)
    if not success:
        return False
    
    expected_keywords = CONFIG["CHECKPOINTS"]["EXPECTED_KEYWORDS"]
    found_keywords = set()
    
    for issue in all_issues or []:
        # 跳过主问题本身
        if issue.get("number") == main_issue_number:
            continue
            
        title = issue.get("title", "")
        body = issue.get("body", "")
        content = f"{title} {body}"
        
        # 检查是否包含预期关键词
        for keyword in expected_keywords:
            if keyword in content:
                found_keywords.add(keyword)
                print(f"[OK] 找到检查点关键词: '{keyword}'")
    
    # 检查是否找到足够的关键词
    if len(found_keywords) >= CONFIG["CHECKPOINTS"]["MIN_CHECKPOINTS"]:
        print(f"[OK] 找到 {len(found_keywords)} 个安全检查点")
        return True
    else:
        print(f"[WARNING] 安全检查点不足: 需要{CONFIG['CHECKPOINTS']['MIN_CHECKPOINTS']}个，找到{len(found_keywords)}个")
        return False

def _validate_comments(main_issue_number: int, headers: Dict[str, str]) -> bool:
    """验证问题评论"""
    success, comments = _call_github_api(f"issues/{main_issue_number}/comments", headers)
    if not success:
        return False

    if len(comments or []) < CONFIG["COMMENTS"]["MIN_COMMENTS"]:
        print(f"[WARNING] 评论数量不足: 需要{CONFIG['COMMENTS']['MIN_COMMENTS']}条，实际{len(comments or [])}条")
        return False

    # 检查评论中是否包含关键词
    all_comments_text = " ".join([comment.get("body", "") for comment in comments or []])
    
    found_keywords = []
    for keyword in CONFIG["COMMENTS"]["REQUIRED_KEYWORDS"]:
        if keyword in all_comments_text:
            found_keywords.append(keyword)
    
    if found_keywords:
        print(f"[OK] 评论中包含关键词: {', '.join(found_keywords)}")
        return True
    else:
        print("[WARNING] 评论中未找到必需的关键词")
        return False

def _validate_security_update(headers: Dict[str, str]) -> bool:
    """验证安全更新"""
    success, prs = _call_github_api("pulls?state=open&per_page=30", headers)
    if not success:
        return False

    for pr in prs or []:
        title = pr.get("title", "")
        
        # 宽松标题匹配
        if CONFIG["SECURITY_UPDATE"]["EXACT_TITLE_MATCH"]:
            title_match = (title == CONFIG["SECURITY_UPDATE"]["TITLE"])
        else:
            title_match = any(keyword in title for keyword in ["安全", "更新", "修复"])
        
        if title_match:
            head_branch = pr.get("head", {}).get("ref", "")
            if head_branch == CONFIG["SECURITY_UPDATE"]["SOURCE_BRANCH"]:
                print(f"[OK] 找到安全更新PR: '{title}'")
                return True

    print("[WARNING] 未找到符合要求的安全更新")
    return False

# -----------------------------
# 3) 主流程
# -----------------------------
def main():
    print("[INFO] 开始验证AI对话系统安全扫描任务...")
    
    headers = _get_github_headers()
    all_passed = True
    main_issue_number = None

    # 1. 验证主安全问题
    print("\n[INFO] 检查主安全问题...")
    issue_found, main_issue_number = _validate_main_issue(headers)
    if not issue_found:
        print("[WARNING] 未找到符合要求的主安全问题")
        all_passed = False
    else:
        print(f"[OK] 找到主安全问题 #{main_issue_number}")

    # 2. 验证安全检查分支
    print("\n[INFO] 检查安全检查分支...")
    if not _validate_branches(headers):
        all_passed = False

    # 3. 验证安全检查点
    print("\n[INFO] 检查安全检查点...")
    if main_issue_number and not _validate_checkpoints(main_issue_number, headers):
        all_passed = False

    # 4. 验证问题评论
    print("\n[INFO] 检查安全问题评论...")
    if main_issue_number and not _validate_comments(main_issue_number, headers):
        all_passed = False

    # 5. 验证安全更新
    print("\n[INFO] 检查安全更新...")
    if CONFIG["SECURITY_UPDATE"]["REQUIRED"] and not _validate_security_update(headers):
        all_passed = False

    # 结果汇总
    print("\n" + "=" * 50)
    if all_passed:
        print("[SUCCESS] AI对话系统安全扫描任务验证通过!")
        print("[INFO] 所有基本要求已满足，部分警告可忽略")
        sys.exit(0)
    else:
        print("[WARNING] AI对话系统安全扫描任务存在一些问题")
        print("[INFO] 请检查警告信息并酌情处理")
        sys.exit(1)

# -----------------------------
# 入口
# -----------------------------
if __name__ == "__main__":
    main()