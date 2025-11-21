"""
Arquivo principal do sistema
Inicializa os catálogos, controladores e interface
"""
import tkinter as tk
from tkinter import ttk, messagebox
from catalogs import CatUsuarios, CatRequerentes, CatFuncoes, CatCaesDomesticos
from controllers import CTRUsuarios, CTRRequisicoes, CTRCaesDom
from ui_permissoes import UIPermissoes
from ui_caes import UICaesDom
from validations import ValidationError


class SistemaMonitoramento:
    """Sistema principal de monitoramento de cães"""
    
    def __init__(self):
        # Inicializar catálogos
        self.cat_funcoes = CatFuncoes()
        self.cat_usuarios = CatUsuarios()
        self.cat_requerentes = CatRequerentes()
        self.cat_caes = CatCaesDomesticos()
        
        # Inicializar controladores
        self.ctr_usuarios = CTRUsuarios(self.cat_usuarios, self.cat_funcoes)
        self.ctr_requisicoes = CTRRequisicoes(self.cat_requerentes, self.cat_usuarios, 
                                              self.cat_funcoes)
        self.ctr_caes = CTRCaesDom(self.cat_caes)
        
        # Criar dados de teste
        self._criar_dados_teste()
    
    def _criar_dados_teste(self):
        """Cria alguns dados de teste para demonstração"""
        try:
            # Adicionar usuários de teste
            self.ctr_usuarios.adicionarUsu("Dr. João Silva", "joao@exemplo.com", 1)  # Admin
            self.ctr_usuarios.adicionarUsu("Maria Santos", "maria@exemplo.com", 3)  # Veterinário
            
            # Adicionar requisições de teste
            self.ctr_requisicoes.criarRequisicao(
                "Pedro Oliveira",
                "pedro@exemplo.com",
                "Solicito acesso ao sistema para colaborar com a pesquisa de campo sobre cães domésticos."
            )
            self.ctr_requisicoes.criarRequisicao(
                "Ana Costa",
                "ana@exemplo.com",
                "Preciso de acesso para registrar dados das entrevistas com tutores de cães."
            )
            
            # Adicionar cães de teste
            self.ctr_caes.adicionarCao("Rex", "15/03/2020", "Masculino", "Ativo")
            self.ctr_caes.adicionarCao("Bella", "22/07/2019", "Feminino", "Ativo")
            self.ctr_caes.adicionarCao("Max", "10/01/2021", "Masculino", "Inativo")
            
        except ValidationError:
            pass  # Ignora erros se dados já existirem
    
    def iniciar_menu_principal(self):
        """Inicia o menu principal do sistema"""
        root = tk.Tk()
        root.title("Sistema de Monitoramento de Cães")
        root.geometry("600x400")
        
        # Frame principal
        frame = ttk.Frame(root, padding=40)
        frame.pack(fill='both', expand=True)
        
        # Título
        ttk.Label(frame, text="SISTEMA DE MONITORAMENTO DE CÃES", 
                 font=('Arial', 16, 'bold')).pack(pady=30)
        
        ttk.Label(frame, text="Selecione o módulo:", 
                 font=('Arial', 12)).pack(pady=20)
        
        # Botões do menu
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(pady=20)
        
        ttk.Button(btn_frame, text="Gerenciar Permissões", 
                  command=lambda: self._abrir_modulo_permissoes(root),
                  width=30).pack(pady=10)
        
        ttk.Button(btn_frame, text="Cadastrar Cães Domésticos",
                  command=lambda: self._abrir_modulo_caes(root),
                  width=30).pack(pady=10)
        
        ttk.Button(btn_frame, text="Criar Nova Requisição",
                  command=lambda: self._abrir_form_requisicao(root),
                  width=30).pack(pady=10)
        
        ttk.Button(btn_frame, text="Sair",
                  command=root.quit,
                  width=30).pack(pady=10)
        
        root.mainloop()
    
    def _abrir_modulo_permissoes(self, parent):
        """Abre módulo de gerenciamento de permissões"""
        janela = tk.Toplevel(parent)
        UIPermissoes(janela, self.ctr_usuarios, self.ctr_requisicoes)
    
    def _abrir_modulo_caes(self, parent):
        """Abre módulo de cadastro de cães"""
        janela = tk.Toplevel(parent)
        UICaesDom(janela, self.ctr_caes)
    
    def _abrir_form_requisicao(self, parent):
        """Abre formulário para criar requisição"""
        from ui_requisicao import FormRequisicao
        FormRequisicao(parent, self.ctr_requisicoes)


if __name__ == "__main__":
    sistema = SistemaMonitoramento()
    sistema.iniciar_menu_principal()
