from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from datetime import datetime
import re

app = Flask(__name__)
CORS(app)

# Armazenamento em memória
class Database:
    def __init__(self):
        self.usuarios = []
        self.requisicoes = []
        self.funcoes = []
        self.caes = []
        self.usuario_counter = 1
        self.requisicao_counter = 1
        self.cao_counter = 1
        
    def init_data(self):
        # Inicializar funções
        self.funcoes = [
            {"idFuncao": 1, "nome": "Administrador", "descricao": "Acesso total ao sistema"},
            {"idFuncao": 2, "nome": "Entrevistador", "descricao": "Realiza entrevistas"},
            {"idFuncao": 3, "nome": "Veterinário", "descricao": "Registra visitas veterinárias"},
            {"idFuncao": 4, "nome": "Legista", "descricao": "Registra necropsias"},
            {"idFuncao": 5, "nome": "Pesquisador Sorológico", "descricao": "Análises sorológicas"}
        ]
        
        # Inicializar usuários
        self.usuarios = [
            {
                "idUsu": 1,
                "nome": "Usuário A",
                "email": "usu.a@exemplo.com",
                "senha": "Usuário A",
                "funcao": self.funcoes[0]
            },
            {
                "idUsu": 2,
                "nome": "Usuário B",
                "email": "usu.b@exemplo.com",
                "senha": "Usuário B",
                "funcao": self.funcoes[3]
            },
            {
                "idUsu": 3,
                "nome": "Usuário C",
                "email": "usu.c@exemplo.com",
                "senha": "Usuário C",
                "funcao": self.funcoes[2]
            }
        ]
        self.usuario_counter = 4
        
        # Inicializar requisições
        self.requisicoes = [
            {
                "idReq": 1,
                "nome": "Usuário F",
                "email": "usu.f@exemplo.com",
                "justificativa": "Preciso de acesso ao sistema para realizar pesquisas sobre ectoparasitos.",
                "data": "12/03/2025"
            },
            {
                "idReq": 2,
                "nome": "Usuário G",
                "email": "usu.g@exemplo.com",
                "justificativa": "Sou veterinário e preciso cadastrar dados das visitas aos cães domésticos.",
                "data": "02/02/2025"
            },
            {
                "idReq": 3,
                "nome": "Usuário H",
                "email": "usu.h@exemplo.com",
                "justificativa": "Necessito acessar o sistema para análises sorológicas dos cães.",
                "data": "01/12/2024"
            }
        ]
        self.requisicao_counter = 4
        
        # Inicializar cães
        self.caes = [
            {
                "idCao": "cao-001",
                "nome": "Rex",
                "dataNasc": "15/03/2020",
                "sexo": "Masculino",
                "status": "Ativo"
            },
            {
                "idCao": "cao-002",
                "nome": "Bella",
                "dataNasc": "22/07/2019",
                "sexo": "Feminino",
                "status": "Ativo"
            },
            {
                "idCao": "cao-003",
                "nome": "Max",
                "dataNasc": "10/01/2021",
                "sexo": "Masculino",
                "status": "Inativo"
            }
        ]
        self.cao_counter = 4

db = Database()
db.init_data()

# Validações
def validar_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def email_existe(email, excluir_id=None):
    for usuario in db.usuarios:
        if usuario["email"] == email and usuario["idUsu"] != excluir_id:
            return True
    return False

# Rotas principais
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/permissoes')
def permissoes():
    return render_template('permissoes.html')

@app.route('/caes')
def caes():
    return render_template('caes.html')

# API - Funções
@app.route('/api/funcoes', methods=['GET'])
def get_funcoes():
    return jsonify(db.funcoes)

# API - Usuários
@app.route('/api/usuarios', methods=['GET'])
def get_usuarios():
    tipo = request.args.get('tipo', '')
    termo = request.args.get('termo', '')
    
    usuarios_filtrados = db.usuarios
    
    if tipo and termo:
        if tipo == 'nome':
            usuarios_filtrados = [u for u in usuarios_filtrados if termo.lower() in u['nome'].lower()]
        elif tipo == 'email':
            usuarios_filtrados = [u for u in usuarios_filtrados if termo.lower() in u['email'].lower()]
        elif tipo == 'funcao':
            usuarios_filtrados = [u for u in usuarios_filtrados if termo.lower() in u['funcao']['nome'].lower()]
    
    return jsonify(usuarios_filtrados)

@app.route('/api/usuarios', methods=['POST'])
def adicionar_usuario():
    dados = request.json
    
    # Validações
    if not dados.get('nome') or not dados.get('email') or not dados.get('idFuncao'):
        return jsonify({"erro": "Todos os campos são obrigatórios"}), 400
    
    if not validar_email(dados['email']):
        return jsonify({"erro": "Email inválido"}), 400
    
    if email_existe(dados['email']):
        return jsonify({"erro": "Email já cadastrado"}), 400
    
    # Buscar função
    funcao = next((f for f in db.funcoes if f['idFuncao'] == dados['idFuncao']), None)
    if not funcao:
        return jsonify({"erro": "Função não encontrada"}), 404
    
    # Criar usuário
    novo_usuario = {
        "idUsu": db.usuario_counter,
        "nome": dados['nome'],
        "email": dados['email'],
        "senha": dados['nome'],  # Senha inicial é o nome
        "funcao": funcao
    }
    
    db.usuarios.append(novo_usuario)
    db.usuario_counter += 1
    
    return jsonify(novo_usuario), 201

@app.route('/api/usuarios/<int:id_usu>', methods=['PUT'])
def editar_usuario(id_usu):
    dados = request.json
    
    # Buscar usuário
    usuario = next((u for u in db.usuarios if u['idUsu'] == id_usu), None)
    if not usuario:
        return jsonify({"erro": "Usuário não encontrado"}), 404
    
    # Validações
    if not dados.get('nome') or not dados.get('email') or not dados.get('idFuncao'):
        return jsonify({"erro": "Todos os campos são obrigatórios"}), 400
    
    if not validar_email(dados['email']):
        return jsonify({"erro": "Email inválido"}), 400
    
    if email_existe(dados['email'], id_usu):
        return jsonify({"erro": "Email já cadastrado"}), 400
    
    # Buscar função
    funcao = next((f for f in db.funcoes if f['idFuncao'] == dados['idFuncao']), None)
    if not funcao:
        return jsonify({"erro": "Função não encontrada"}), 404
    
    # Atualizar usuário
    usuario['nome'] = dados['nome']
    usuario['email'] = dados['email']
    usuario['funcao'] = funcao
    
    return jsonify(usuario)

@app.route('/api/usuarios/<int:id_usu>', methods=['DELETE'])
def remover_usuario(id_usu):
    usuario = next((u for u in db.usuarios if u['idUsu'] == id_usu), None)
    if not usuario:
        return jsonify({"erro": "Usuário não encontrado"}), 404
    
    db.usuarios.remove(usuario)
    return jsonify({"mensagem": "Usuário removido com sucesso"})

@app.route('/api/usuarios/<int:id_usu>/recuperar-senha', methods=['POST'])
def recuperar_senha(id_usu):
    usuario = next((u for u in db.usuarios if u['idUsu'] == id_usu), None)
    if not usuario:
        return jsonify({"erro": "Usuário não encontrado"}), 404
    
    usuario['senha'] = usuario['nome']  # Resetar senha para o nome
    return jsonify({"mensagem": "Senha recuperada com sucesso", "nova_senha": usuario['senha']})

# API - Requisições
@app.route('/api/requisicoes', methods=['GET'])
def get_requisicoes():
    tipo = request.args.get('tipo', '')
    termo = request.args.get('termo', '')
    
    requisicoes_filtradas = db.requisicoes
    
    if tipo and termo:
        if tipo == 'nome':
            requisicoes_filtradas = [r for r in requisicoes_filtradas if termo.lower() in r['nome'].lower()]
        elif tipo == 'email':
            requisicoes_filtradas = [r for r in requisicoes_filtradas if termo.lower() in r['email'].lower()]
    
    return jsonify(requisicoes_filtradas)

@app.route('/api/requisicoes/<int:id_req>/aceitar', methods=['POST'])
def aceitar_requisicao(id_req):
    dados = request.json
    
    # Buscar requisição
    requisicao = next((r for r in db.requisicoes if r['idReq'] == id_req), None)
    if not requisicao:
        return jsonify({"erro": "Requisição não encontrada"}), 404
    
    # Buscar função
    funcao = next((f for f in db.funcoes if f['idFuncao'] == dados['idFuncao']), None)
    if not funcao:
        return jsonify({"erro": "Função não encontrada"}), 404
    
    # Criar usuário a partir da requisição
    novo_usuario = {
        "idUsu": db.usuario_counter,
        "nome": requisicao['nome'],
        "email": requisicao['email'],
        "senha": requisicao['nome'],
        "funcao": funcao
    }
    
    db.usuarios.append(novo_usuario)
    db.usuario_counter += 1
    
    # Remover requisição
    db.requisicoes.remove(requisicao)
    
    return jsonify(novo_usuario), 201

@app.route('/api/requisicoes/<int:id_req>/recusar', methods=['POST'])
def recusar_requisicao(id_req):
    requisicao = next((r for r in db.requisicoes if r['idReq'] == id_req), None)
    if not requisicao:
        return jsonify({"erro": "Requisição não encontrada"}), 404
    
    db.requisicoes.remove(requisicao)
    return jsonify({"mensagem": "Requisição recusada com sucesso"})

# API - Cães
@app.route('/api/caes', methods=['GET'])
def get_caes():
    tipo = request.args.get('tipo', '')
    termo = request.args.get('termo', '')
    
    caes_filtrados = db.caes
    
    if tipo and termo:
        if tipo == 'nome':
            caes_filtrados = [c for c in caes_filtrados if termo.lower() in c['nome'].lower()]
        elif tipo == 'codigo':
            caes_filtrados = [c for c in caes_filtrados if termo.lower() in c['idCao'].lower()]
        elif tipo == 'status':
            caes_filtrados = [c for c in caes_filtrados if termo.lower() in c['status'].lower()]
    
    return jsonify(caes_filtrados)

@app.route('/api/caes', methods=['POST'])
def adicionar_cao():
    dados = request.json
    
    # Validações
    if not dados.get('nome') or not dados.get('dataNasc') or not dados.get('sexo') or not dados.get('status'):
        return jsonify({"erro": "Todos os campos são obrigatórios"}), 400
    
    # Criar cão
    novo_cao = {
        "idCao": f"cao-{str(db.cao_counter).zfill(3)}",
        "nome": dados['nome'],
        "dataNasc": dados['dataNasc'],
        "sexo": dados['sexo'],
        "status": dados['status']
    }
    
    db.caes.append(novo_cao)
    db.cao_counter += 1
    
    return jsonify(novo_cao), 201

@app.route('/api/caes/<id_cao>', methods=['PUT'])
def editar_cao(id_cao):
    dados = request.json
    
    # Buscar cão
    cao = next((c for c in db.caes if c['idCao'] == id_cao), None)
    if not cao:
        return jsonify({"erro": "Cão não encontrado"}), 404
    
    # Validações
    if not dados.get('nome') or not dados.get('dataNasc') or not dados.get('sexo') or not dados.get('status'):
        return jsonify({"erro": "Todos os campos são obrigatórios"}), 400
    
    # Atualizar cão
    cao['nome'] = dados['nome']
    cao['dataNasc'] = dados['dataNasc']
    cao['sexo'] = dados['sexo']
    cao['status'] = dados['status']
    
    return jsonify(cao)

@app.route('/api/caes/<id_cao>', methods=['DELETE'])
def remover_cao(id_cao):
    cao = next((c for c in db.caes if c['idCao'] == id_cao), None)
    if not cao:
        return jsonify({"erro": "Cão não encontrado"}), 404
    
    db.caes.remove(cao)
    return jsonify({"mensagem": "Cão removido com sucesso"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
