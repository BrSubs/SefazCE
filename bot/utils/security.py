import re

def sanitize_input(text: str) -> str:
    """Remove caracteres potencialmente perigosos"""
    return re.sub(r'[^\w\s-]', '', text)