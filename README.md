# AI对话系统安全扫描工具

一个专门为AI对话系统设计的安全漏洞扫描与验证工具，帮助开发者发现、记录和修复潜在的安全风险。

## 📋 功能特性

- 🔍 **自动化安全扫描** - 自动检测常见的安全漏洞
- 📊 **风险评估** - 对发现的问题进行严重程度分类
- 📝 **报告生成** - 自动生成详细的安全扫描报告
- 🔗 **问题跟踪** - 与GitHub Issues集成，便于问题管理
- ⚡ **持续集成** - 支持GitHub Actions自动化运行
- 🛡️ **多维度检查** - 覆盖输入验证、权限控制、数据安全等多个方面

## 🚀 快速开始

### 环境要求

- Python 3.8+
- GitHub账户
- GitHub Personal Access Token

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/your-organization/ai-chatbot-security-scanner.git
cd ai-chatbot-security-scanner
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **配置环境变量**
```bash
export GITHUB_TOKEN="your_github_personal_access_token"
export GITHUB_ORG="your-organization"
export GITHUB_REPO="ai-chatbot-security-scanner"
```

4. **运行安全扫描**
```bash
python scripts/security_validation.py
```

## 📁 项目结构

```
ai-chatbot-security-scanner/
├── src/                    # 源代码目录
│   ├── utils/
│   │   └── security.py     # 安全工具函数
│   └── api/
│       └── auth.py         # 认证授权模块
├── config/
│   └── settings.py         # 配置文件
├── scripts/
│   ├── security_validation.py  # 主验证脚本
│   └── create_test_issues.py   # 测试Issue创建脚本
├── docs/security/          # 安全文档目录
├── .github/workflows/      # GitHub工作流配置
└── README.md
```

## 🔧 配置说明

### GitHub配置

在运行前，请确保配置正确的GitHub信息：

```python
# 在 security_validation.py 中更新这些配置
CONFIG = {
    "GITHUB_ENV": {
        "ORGANIZATION": "your-actual-organization",  # 替换为实际组织名
        "REPOSITORY": "ai-chatbot-security-scanner", # 仓库名
        "TOKEN_ENV_VAR": "GITHUB_TOKEN",            # Token环境变量名
    }
}
```

### Token权限要求

您的GitHub Token需要以下权限：
- `repo` (完整仓库访问)
- `read:org` (组织读取权限)
- `user:read` (用户信息读取)

## 📊 扫描内容

### 安全检查项

1. **主安全问题验证**
   - 问题标题匹配
   - 标签验证
   - 关联问题检查

2. **分支安全检查**
   - security-scan分支
   - privacy-check分支  
   - api-audit分支

3. **安全检查点**
   - 用户输入处理安全
   - 对话响应安全性
   - 权限验证机制
   - API接口安全

4. **安全更新验证**
   - PR标题验证
   - 分支来源检查
   - 关联问题验证

## 📝 生成文档

工具会自动生成以下安全文档：

- `安全扫描报告.md` - 基础安全扫描结果和风险评估
- `问题跟踪记录.md` - 问题发现和修复状态跟踪
- `隐私检查报告.md` - 数据保护和合规性检查
- `安全检查计划.md` - 安全测试策略和方案

## 🛠️ 开发指南

### 添加新的安全检查

1. 在 `security_validation.py` 中添加新的验证函数
2. 更新配置中的检查项
3. 添加对应的测试用例

### 自定义检查规则

修改 `CONFIG` 字典中的相关配置：

```python
CONFIG = {
    "MAIN_ISSUE": {
        "TITLE": "你的自定义标题",
        "REQUIRED_LABELS": ["自定义标签1", "自定义标签2"],
        # ... 其他配置
    }
}
```

## 🤝 贡献指南

1. Fork本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🆘 技术支持

如果您遇到问题：

1. 查看 [Issues](https://github.com/your-organization/ai-chatbot-security-scanner/issues) 页面
2. 创建新的Issue描述您的问题
3. 确保包含详细的错误信息和日志

## 🔄 版本历史

- **v1.0.0** (2024-01-01)
  - 初始版本发布
  - 基础安全扫描功能
  - GitHub集成支持
  - 自动化报告生成

---

**注意**: 在使用前请确保您有权限访问目标GitHub仓库，并配置了正确的认证信息。

## 这个README.md文件应该放在项目的根目录下，它提供了项目的完整说明、使用指南和配置信息。