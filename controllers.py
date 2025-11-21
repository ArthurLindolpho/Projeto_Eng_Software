"""
Controladores do sistema
Implementam a lógica de negócio seguindo os diagramas de comunicação
"""
from typing import Optional, List
from catalogs import CatUsuarios, CatRequerentes, CatFuncoes, CatCaesDomesticos
from validations import validar_email, validar_campos_obrigatorios, validar_sexo, validar_status, ValidationError


class CTRUsuarios:
    """Controlador de usuários"""
    def __init__(self, cat_usuarios: CatUsuarios, cat_funcoes: CatFuncoes):
        self.cat_usuarios = cat_usuarios
        self.cat_funcoes = cat_funcoes
    
    def visualizarListaUsu(self) -> List[dict]:
        """Visualiza lista de usuários"""
        return self.cat_usuarios.visualizarListaUsu()
    
    def filtrarListaUsu(self, tipo: str, termo: str) -> List[dict]:
        """Filtra lista de usuários"""
        return self.cat_usuarios.filtrarListaUsu(tipo, termo)
    
    def adicionarUsu(self, nome: str, email: str, idFuncao: int):
        """Adiciona novo usuário - Segue diagrama de comunicação"""
        # Validações
        validar_campos_obrigatorios({'nome': nome, 'email': email})
        validar_email(email)
        
        # Verifica duplicidade de email
        if self.cat_usuarios.encontrarPorEmail(email):
            raise ValidationError("Email já cadastrado no sistema")
        
        # 1.1: objFunc = encontrarFunc(idFuncao)
        objFunc = self.cat_funcoes.encontrarFunc(idFuncao)
        if not objFunc:
            raise ValidationError("Função não encontrada")
        
        # 1.2: adicionarUsu(nome, email, objFunc)
        self.cat_usuarios.adicionarUsu(nome, email, objFunc)
    
    def editarUsu(self, idUsu: int, nome: str, email: str, idFuncao: int):
        """Edita usuário - Segue diagrama de comunicação"""
        # Validações
        validar_campos_obrigatorios({'nome': nome, 'email': email})
        validar_email(email)
        
        # Verifica duplicidade de email (exceto o próprio usuário)
        usuario_email = self.cat_usuarios.encontrarPorEmail(email)
        if usuario_email and usuario_email.idUsu != idUsu:
            raise ValidationError("Email já cadastrado no sistema")
        
        # 1.1: objFunc = encontrarFunc(idFuncao)
        objFunc = self.cat_funcoes.encontrarFunc(idFuncao)
        if not objFunc:
            raise ValidationError("Função não encontrada")
        
        # 1.2: objUsu = encontrarUsu(idUsu)
        objUsu = self.cat_usuarios.encontrarUsu(idUsu)
        if not objUsu:
            raise ValidationError("Usuário não encontrado")
        
        # 1.3: editarUsu(nome, email, objFunc)
        objUsu.editarUsu(nome, email, objFunc)
    
    def removerUsu(self, idUsu: int):
        """Remove usuário - Segue diagrama de comunicação"""
        # 1.1: removerUsu(idUsu)
        if not self.cat_usuarios.removerUsu(idUsu):
            raise ValidationError("Usuário não encontrado")
    
    def recuperarSenha(self, idUsu: int):
        """Recupera senha do usuário"""
        usuario = self.cat_usuarios.encontrarUsu(idUsu)
        if not usuario:
            raise ValidationError("Usuário não encontrado")
        usuario.recuperarSenha()


class CTRRequisicoes:
    """Controlador de requisições"""
    def __init__(self, cat_requerentes: CatRequerentes, cat_usuarios: CatUsuarios, 
                 cat_funcoes: CatFuncoes):
        self.cat_requerentes = cat_requerentes
        self.cat_usuarios = cat_usuarios
        self.cat_funcoes = cat_funcoes
    
    def visualizarListaReq(self) -> List[dict]:
        """Visualiza lista de requisições"""
        return self.cat_requerentes.visualizarListaReq()
    
    def filtrarListaReq(self, tipo: str, termo: str) -> List[dict]:
        """Filtra lista de requisições"""
        return self.cat_requerentes.filtrarListaReq(tipo, termo)
    
    def expandir(self, idReq: int) -> dict:
        """Expande detalhes de uma requisição"""
        req = self.cat_requerentes.encontrarReq(idReq)
        if not req:
            raise ValidationError("Requisição não encontrada")
        return req.visualizarReq()
    
    def aceitarReq(self, idReq: int, idFuncao: int):
        """Aceita requisição e cria usuário - Segue diagrama de comunicação"""
        # 1.1: objFunc = encontrarFunc(idFuncao)
        objFunc = self.cat_funcoes.encontrarFunc(idFuncao)
        if not objFunc:
            raise ValidationError("Função não encontrada")
        
        # 1.2: objReq = encontrarReq(idReq)
        objReq = self.cat_requerentes.encontrarReq(idReq)
        if not objReq:
            raise ValidationError("Requisição não encontrada")
        
        # Verifica duplicidade de email
        if self.cat_usuarios.encontrarPorEmail(objReq.email):
            raise ValidationError("Email já cadastrado no sistema")
        
        # 1.3: nome = getNome()
        nome = objReq.nome
        
        # 1.4: email = getEmail()
        email = objReq.email
        
        # 1.5: adicionarUsu(nome, email, objFunc)
        self.cat_usuarios.adicionarUsu(nome, email, objFunc)
        
        # 1.6: removerReq(idReq)
        self.cat_requerentes.removerReq(idReq)
    
    def recusarReq(self, idReq: int):
        """Recusa requisição - Segue diagrama de comunicação"""
        # 1.1: removerReq(idReq)
        if not self.cat_requerentes.removerReq(idReq):
            raise ValidationError("Requisição não encontrada")
    
    def criarRequisicao(self, nome: str, email: str, justificativa: str):
        """Cria nova requisição de acesso"""
        # Validações
        validar_campos_obrigatorios({'nome': nome, 'email': email, 'justificativa': justificativa})
        validar_email(email)
        
        # Verifica se já existe requisição com este email
        if self.cat_requerentes.encontrarPorEmail(email):
            raise ValidationError("Já existe uma requisição pendente com este email")
        
        # Verifica se email já está cadastrado
        if self.cat_usuarios.encontrarPorEmail(email):
            raise ValidationError("Email já cadastrado no sistema")
        
        self.cat_requerentes.adicionarReq(nome, email, justificativa)


class CTRCaesDom:
    """Controlador de cães domésticos"""
    def __init__(self, cat_caes: CatCaesDomesticos):
        self.cat_caes = cat_caes
    
    def visualizarListaCaes(self) -> List[dict]:
        """Visualiza lista de cães"""
        return self.cat_caes.visualizarListaCaes()
    
    def filtrarListaCaes(self, tipo: str, termo: str) -> List[dict]:
        """Filtra lista de cães"""
        return self.cat_caes.filtrarListaCaes(tipo, termo)
    
    def expandir(self, idCao: str) -> dict:
        """Expande detalhes de um cão"""
        cao = self.cat_caes.encontrarCao(idCao)
        if not cao:
            raise ValidationError("Cão não encontrado")
        return cao.visualizarCao()
    
    def adicionarCao(self, nome: str, dataNasc: str, sexo: str, status: str):
        """Adiciona novo cão - Segue diagrama de comunicação"""
        # Validações
        validar_campos_obrigatorios({'nome': nome, 'dataNasc': dataNasc, 
                                     'sexo': sexo, 'status': status})
        validar_sexo(sexo)
        validar_status(status)
        
        # 1.1: adicionarCao(nome, dataNasc, sexo, status)
        self.cat_caes.adicionarCao(nome, dataNasc, sexo, status)
    
    def editarCao(self, idCao: str, nome: str, dataNasc: str, sexo: str, status: str):
        """Edita cão - Segue diagrama de comunicação"""
        # Validações
        validar_campos_obrigatorios({'nome': nome, 'dataNasc': dataNasc,
                                     'sexo': sexo, 'status': status})
        validar_sexo(sexo)
        validar_status(status)
        
        # 1.1: objCao = encontrarCao(idCao)
        objCao = self.cat_caes.encontrarCao(idCao)
        if not objCao:
            raise ValidationError("Cão não encontrado")
        
        # 1.2: editarCao(nome, dataNasc, sexo, status)
        objCao.editarCao(nome, dataNasc, sexo, status)
    
    def removerCao(self, idCao: str):
        """Remove cão - Segue diagrama de comunicação"""
        # 1.1: removerCao(idCao)
        if not self.cat_caes.removerCao(idCao):
            raise ValidationError("Cão não encontrado")
