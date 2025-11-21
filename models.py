"""
Modelos de domínio do sistema de monitoramento de cães
Implementa as classes Usuario, Requerente, Funcao e Cao
"""
import re
from typing import Optional
from datetime import datetime


class Funcao:
    """Representa uma função/cargo no sistema"""
    _id_counter = 1
    
    def __init__(self, nome: str, descricao: str):
        self.idFuncao = Funcao._id_counter
        Funcao._id_counter += 1
        self.nome = nome
        self.descricao = descricao


class Usuario:
    """Representa um usuário do sistema"""
    _id_counter = 1
    
    def __init__(self, nome: str, email: str, funcao: Funcao):
        self.idUsu = Usuario._id_counter
        Usuario._id_counter += 1
        self.nome = nome
        self.email = email
        self.senha = nome  # Senha inicial é o nome completo
        self.funcao = funcao
    
    def visualizarUsu(self) -> dict:
        """Retorna dados do usuário para visualização"""
        return {
            'idUsu': self.idUsu,
            'nome': self.nome,
            'email': self.email,
            'funcao': self.funcao.nome
        }
    
    def editarUsu(self, nome: Optional[str] = None, email: Optional[str] = None, 
                  funcao: Optional[Funcao] = None):
        """Edita dados do usuário"""
        if nome:
            self.nome = nome
        if email:
            self.email = email
        if funcao:
            self.funcao = funcao
    
    def recuperarSenha(self):
        """Recupera senha do usuário (reseta para o nome)"""
        self.senha = self.nome


class Requerente:
    """Representa uma requisição de acesso ao sistema"""
    _id_counter = 1
    
    def __init__(self, nome: str, email: str, justificativa: str):
        self.idReq = Requerente._id_counter
        Requerente._id_counter += 1
        self.nome = nome
        self.email = email
        self.justificativa = justificativa
        self.data = datetime.now()
    
    def visualizarReq(self) -> dict:
        """Retorna dados da requisição para visualização"""
        return {
            'idReq': self.idReq,
            'nome': self.nome,
            'email': self.email,
            'justificativa': self.justificativa,
            'data': self.data.strftime('%d/%m/%Y')
        }


class Cao:
    """Representa um cão doméstico"""
    _id_counter = 1
    
    def __init__(self, nome: str, dataNasc: str, sexo: str, status: str):
        self.idCao = f"cao-{Cao._id_counter:03d}"
        Cao._id_counter += 1
        self.nome = nome
        self.dataNasc = dataNasc
        self.sexo = sexo  # Masculino ou Feminino
        self.status = status  # Ativo ou Inativo
    
    def visualizarCao(self) -> dict:
        """Retorna dados do cão para visualização"""
        return {
            'idCao': self.idCao,
            'nome': self.nome,
            'dataNasc': self.dataNasc,
            'sexo': self.sexo,
            'status': self.status
        }
    
    def editarCao(self, nome: Optional[str] = None, dataNasc: Optional[str] = None,
                  sexo: Optional[str] = None, status: Optional[str] = None):
        """Edita dados do cão"""
        if nome:
            self.nome = nome
        if dataNasc:
            self.dataNasc = dataNasc
        if sexo:
            self.sexo = sexo
        if status:
            self.status = status
