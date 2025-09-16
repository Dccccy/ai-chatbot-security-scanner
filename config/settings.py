# 安全相关配置
SECURITY_CONFIG = {
    "input_validation": True,
    "output_sanitization": True,
    "rate_limiting": True,
    "auth_required": True,
    "encryption_enabled": True
}

# API配置
API_CONFIG = {
    "timeout": 30,
    "max_retries": 3,
    "allowed_domains": ["example.com"]
}