"""
Catálogos do sistema
Gerenciam as coleções de objetos em memória
"""
from typing import List, Optional
from models import Usuario, Requerente, Funcao, Cao


class CatFuncoes:
    """Catálogo de funções do sistema"""
    def __init__(self):
        self._funcoes: List[Funcao] = []
        self._inicializar_funcoes_padrao()
    
    def _inicializar_funcoes_padrao(self):
        """Inicializa as funções padrão do sistema"""
        funcoes_padrao = [
            ("Administrador", "Acesso total ao sistema"),
            ("Entrevistador", "Realiza entrevistas e cadastra tutores e cães"),
            ("Veterinário", "Registra visitas veterinárias"),
            ("Pesquisador Fezes", "Cadastra análises de fezes"),
            ("Pesquisador Vírus", "Registra resultados de exames de vírus"),
            ("Pesquisador Imunopatologia", "Registra resultados de imunopatologia"),
            ("Pesquisador Tripasomatídeos", "Registra resultados de tripasomatídeos"),
            ("Pesquisador Sorológico", "Registra análises sorológicas"),
            ("Pesquisador Ectoparasitos", "Cadastra análises de ectoparasitos"),
            ("Legista", "Registra atropelamentos e necrópsias"),
            ("Pesquisador Helmintos", "Cadastra análises de helmintos")
        ]
        
        for nome, descricao in funcoes_padrao:
            self._funcoes.append(Funcao(nome, descricao))
    
    def encontrarFunc(self, idFuncao: int) -> Optional[Funcao]:
        """Encontra uma função pelo ID"""
        for funcao in self._funcoes:
            if funcao.idFuncao == idFuncao:
                return funcao
        return None
    
    def listar_todas(self) -> List[Funcao]:
        """Retorna todas as funções"""
        return self._funcoes.copy()


class CatUsuarios:
    """Catálogo de usuários do sistema"""
    def __init__(self):
        self._usuarios: List[Usuario] = []
    
    def visualizarListaUsu(self) -> List[dict]:
        """Retorna lista de todos os usuários"""
        return [usu.visualizarUsu() for usu in self._usuarios]
    
    def filtrarListaUsu(self, tipo: str, termo: str) -> List[dict]:
        """Filtra usuários por tipo (nome/email) e termo"""
        resultado = []
        termo_lower = termo.lower()
        
        for usu in self._usuarios:
            if tipo == "nome" and termo_lower in usu.nome.lower():
                resultado.append(usu.visualizarUsu())
            elif tipo == "email" and termo_lower in usu.email.lower():
                resultado.append(usu.visualizarUsu())
        
        return resultado
    
    def encontrarUsu(self, idUsu: int) -> Optional[Usuario]:
        """Encontra um usuário pelo ID"""
        for usu in self._usuarios:
            if usu.idUsu == idUsu:
                return usu
        return None
    
    def encontrarPorEmail(self, email: str) -> Optional[Usuario]:
        """Encontra um usuário pelo email"""
        for usu in self._usuarios:
            if usu.email == email:
                return usu
        return None
    
    def editarUsu(self, idUsu: int, nome: Optional[str] = None, 
                  email: Optional[str] = None, funcao: Optional[Funcao] = None):
        """Edita um usuário"""
        usuario = self.encontrarUsu(idUsu)
        if usuario:
            usuario.editarUsu(nome, email, funcao)
    
    def adicionarUsu(self, nome: str, email: str, objFuncao: Funcao) -> Usuario:
        """Adiciona um novo usuário"""
        novo_usuario = Usuario(nome, email, objFuncao)
        self._usuarios.append(novo_usuario)
        return novo_usuario
    
    def removerUsu(self, idUsu: int) -> bool:
        """Remove um usuário"""
        usuario = self.encontrarUsu(idUsu)
        if usuario:
            self._usuarios.remove(usuario)
            return True
        return False


class CatRequerentes:
    """Catálogo de requisições de acesso"""
    def __init__(self):
        self._requerentes: List[Requerente] = []
    
    def visualizarListaReq(self) -> List[dict]:
        """Retorna lista de todas as requisições"""
        return [req.visualizarReq() for req in self._requerentes]
    
    def filtrarListaReq(self, tipo: str, termo: str) -> List[dict]:
        """Filtra requisições por tipo (nome/email) e termo"""
        resultado = []
        termo_lower = termo.lower()
        
        for req in self._requerentes:
            if tipo == "nome" and termo_lower in req.nome.lower():
                resultado.append(req.visualizarReq())
            elif tipo == "email" and termo_lower in req.email.lower():
                resultado.append(req.visualizarReq())
        
        return resultado
    
    def encontrarReq(self, idReq: int) -> Optional[Requerente]:
        """Encontra uma requisição pelo ID"""
        for req in self._requerentes:
            if req.idReq == idReq:
                return req
        return None
    
    def encontrarPorEmail(self, email: str) -> Optional[Requerente]:
        """Encontra uma requisição pelo email"""
        for req in self._requerentes:
            if req.email == email:
                return req
        return None
    
    def adicionarReq(self, nome: str, email: str, justificativa: str) -> Requerente:
        """Adiciona uma nova requisição"""
        novo_requerente = Requerente(nome, email, justificativa)
        self._requerentes.append(novo_requerente)
        return novo_requerente
    
    def removerReq(self, idReq: int) -> bool:
        """Remove uma requisição"""
        requerente = self.encontrarReq(idReq)
        if requerente:
            self._requerentes.remove(requerente)
            return True
        return False


class CatCaesDomesticos:
    """Catálogo de cães domésticos"""
    def __init__(self):
        self._caes: List[Cao] = []
    
    def visualizarListaCaes(self) -> List[dict]:
        """Retorna lista de todos os cães"""
        return [cao.visualizarCao() for cao in self._caes]
    
    def filtrarListaCaes(self, tipo: str, termo: str) -> List[dict]:
        """Filtra cães por tipo (nome/codigo/status) e termo"""
        resultado = []
        termo_lower = termo.lower()
        
        for cao in self._caes:
            if tipo == "nome" and termo_lower in cao.nome.lower():
                resultado.append(cao.visualizarCao())
            elif tipo == "codigo" and termo_lower in cao.idCao.lower():
                resultado.append(cao.visualizarCao())
            elif tipo == "status" and termo_lower in cao.status.lower():
                resultado.append(cao.visualizarCao())
        
        return resultado
    
    def encontrarCao(self, idCao: str) -> Optional[Cao]:
        """Encontra um cão pelo ID"""
        for cao in self._caes:
            if cao.idCao == idCao:
                return cao
        return None
    
    def adicionarCao(self, nome: str, dataNasc: str, sexo: str, status: str) -> Cao:
        """Adiciona um novo cão"""
        novo_cao = Cao(nome, dataNasc, sexo, status)
        self._caes.append(novo_cao)
        return novo_cao
    
    def editarCao(self, idCao: str, nome: Optional[str] = None, 
                  dataNasc: Optional[str] = None, sexo: Optional[str] = None,
                  status: Optional[str] = None):
        """Edita um cão"""
        cao = self.encontrarCao(idCao)
        if cao:
            cao.editarCao(nome, dataNasc, sexo, status)
    
    def removerCao(self, idCao: str) -> bool:
        """Remove um cão"""
        cao = self.encontrarCao(idCao)
        if cao:
            self._caes.remove(cao)
            return True
        return False
