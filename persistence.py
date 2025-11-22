"""
Módulo de persistência de dados em arquivo JSON
"""
import json
import os
from datetime import datetime

DATA_FILE = 'database.json'

class DataPersistence:
    """Gerencia a persistência de dados em arquivo JSON"""
    
    @staticmethod
    def salvar_dados(db):
        """Salva todos os dados no arquivo JSON"""
        dados = {
            'usuarios': db.usuarios,
            'requisicoes': db.requisicoes,
            'funcoes': db.funcoes,
            'caes': db.caes,
            'usuario_counter': db.usuario_counter,
            'requisicao_counter': db.requisicao_counter,
            'cao_counter': db.cao_counter,
            'ultima_atualizacao': datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
        
        try:
            with open(DATA_FILE, 'w', encoding='utf-8') as f:
                json.dump(dados, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"Erro ao salvar dados: {e}")
            return False
    
    @staticmethod
    def carregar_dados(db):
        """Carrega os dados do arquivo JSON"""
        if not os.path.exists(DATA_FILE):
            return False
        
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                dados = json.load(f)
            
            db.usuarios = dados.get('usuarios', [])
            db.requisicoes = dados.get('requisicoes', [])
            db.funcoes = dados.get('funcoes', [])
            db.caes = dados.get('caes', [])
            db.usuario_counter = dados.get('usuario_counter', 1)
            db.requisicao_counter = dados.get('requisicao_counter', 1)
            db.cao_counter = dados.get('cao_counter', 1)
            
            print(f"Dados carregados com sucesso! Última atualização: {dados.get('ultima_atualizacao', 'Desconhecida')}")
            return True
        except Exception as e:
            print(f"Erro ao carregar dados: {e}")
            return False
    
    @staticmethod
    def resetar_dados(db):
        """Remove o arquivo de dados e reinicializa com dados padrão"""
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
        db.init_data()
        DataPersistence.salvar_dados(db)
