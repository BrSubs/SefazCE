import re

def validate_placa(placa: str) -> bool:
    """Valida placa no formato antigo (ABC1234) ou Mercosul (ABC1D34)"""
    placa = placa.upper().strip()
    
    # Formato antigo (3 letras + 4 números)
    if re.match(r'^[A-Z]{3}\d{4}$', placa):
        return True
    
    # Formato Mercosul (3 letras + 1 número + 1 letra + 2 números)
    if re.match(r'^[A-Z]{3}\d[A-Z]\d{2}$', placa):
        return True
    
    return False

def validate_renavam(renavam: str) -> bool:
    """Valida RENAVAM com dígito verificador"""
    renavam = renavam.zfill(11)
    
    if len(renavam) != 11 or not renavam.isdigit():
        return False
    
    # Cálculo do dígito verificador
    pesos = [3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    total = sum(int(renavam[i]) * pesos[i] for i in range(10))
    dv = 11 - (total % 11)
    dv = 0 if dv >= 10 else dv
    
    return dv == int(renavam[-1])

def validate_chassi(chassi: str) -> bool:
    """Valida CHASSI conforme norma ISO 3779-2009"""
    chassi = chassi.upper().strip()
    
    # Verifica formato básico
    if not re.match(r'^[A-HJ-NPR-Z0-9]{17}$', chassi):
        return False
    
    # Verifica se não é sequência de zeros
    if re.match(r'^0+$', chassi[11:]):
        return False
    
    return True

def validate_text_input(text: str) -> dict:
    """Valida e classifica a entrada do usuário"""
    text = text.upper().replace(' ', '')
    
    # Tentar identificar CHASSI primeiro
    chassi_candidate = re.search(r'\b([A-HJ-NPR-Z0-9]{17})\b', text)
    if chassi_candidate and validate_chassi(chassi_candidate.group(1)):
        return {'chassi': chassi_candidate.group(1)}
    
    # Tentar identificar Placa + RENAVAM
    placa_match = re.search(r'\b([A-Z]{3}[0-9A-Z][0-9]{2}[A-Z0-9])\b', text)
    renavam_match = re.search(r'\b(\d{11})\b', text)
    
    if placa_match and renavam_match:
        placa = placa_match.group(1)
        renavam = renavam_match.group(1)
        
        if validate_placa(placa) and validate_renavam(renavam):
            return {
                'placa': format_placa(placa),
                'renavam': renavam
            }
    
    return None

def format_placa(placa: str) -> str:
    """Formata a placa com traço quando necessário"""
    placa = placa.upper().replace('-', '')
    if len(placa) == 7 and placa[4].isalpha():
        return f"{placa[:3]}-{placa[3:]}"
    return placa
