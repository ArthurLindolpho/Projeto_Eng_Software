"""
Validações do sistema
"""
import re


class ValidationError(Exception):
    """Exceção customizada para erros de validação"""
    pass


def validar_email(email: str) -> bool:
    """Valida formato de email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        raise ValidationError("Formato de email inválido")
    return True


def validar_campos_obrigatorios(campos: dict):
    """Valida se todos os campos obrigatórios foram preenchidos"""
    for nome_campo, valor in campos.items():
        if not valor or (isinstance(valor, str) and not valor.strip()):
            raise ValidationError(f"Campo '{nome_campo}' é obrigatório")
    return True


def validar_sexo(sexo: str) -> bool:
    """Valida se o sexo é válido"""
    if sexo not in ['Masculino', 'Feminino']:
        raise ValidationError("Sexo deve ser 'Masculino' ou 'Feminino'")
    return True


def validar_status(status: str) -> bool:
    """Valida se o status é válido"""
    if status not in ['Ativo', 'Inativo']:
        raise ValidationError("Status deve ser 'Ativo' ou 'Inativo'")
    return True
