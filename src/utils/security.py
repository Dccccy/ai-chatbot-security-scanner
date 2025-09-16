def validate_user_input(input_text):
    """用户输入验证"""
    # 基本的XSS防护
    dangerous_chars = ['<', '>', 'script', 'javascript']
    for char in dangerous_chars:
        if char in input_text:
            return False
    return True

def sanitize_output(output_text):
    """输出清理"""
    # 简单的输出清理逻辑
    return output_text.replace('<', '&lt;').replace('>', '&gt;')