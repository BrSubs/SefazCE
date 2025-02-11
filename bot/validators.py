import re

# Regex de validação
RENAVAM_REGEX = re.compile(r"^\d{11}$")
PLACA_REGEX = re.compile(
    r"^[a-zA-Z]{3}\d[a-zA-Z]\d{2}$|^[a-zA-Z]{3}\d{4}$", re.IGNORECASE
)


def validate_renavam(renavam: str) -> bool:
    """Valida o formato do RENAVAM."""
    return bool(RENAVAM_REGEX.match(renavam))


def validate_placa(placa: str) -> bool:
    """Valida o formato da placa (Mercosul ou antigo)."""
    return bool(PLACA_REGEX.match(placa))