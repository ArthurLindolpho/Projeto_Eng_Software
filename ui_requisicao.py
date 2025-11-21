"""
Formulário para criação de requisição de acesso
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from controllers import CTRRequisicoes
from validations import ValidationError


class FormRequisicao:
    """Formulário para requisição de acesso ao sistema"""
    
    def __init__(self, parent, ctr_requisicoes: CTRRequisicoes):
        self.ctr_requisicoes = ctr_requisicoes
        
        # Janela
        self.janela = tk.Toplevel(parent)
        self.janela.title("Requisição de Acesso")
        self.janela.geometry("500x500")
        self.janela.transient(parent)
        self.janela.grab_set()
        
        # Frame principal
        frame = ttk.Frame(self.janela, padding=20)
        frame.pack(fill='both', expand=True)
        
        # Título
        ttk.Label(frame, text="REQUISIÇÃO DE ACESSO", 
                 font=('Arial', 14, 'bold')).pack(pady=10)
        
        ttk.Label(frame, text="Preencha os dados abaixo para solicitar acesso ao sistema:",
                 font=('Arial', 9)).pack(pady=5)
        
        # Nome completo
        ttk.Label(frame, text="Nome Completo:").pack(anchor='w', pady=(15, 2))
        self.entry_nome = ttk.Entry(frame, width=50)
        self.entry_nome.pack(fill='x', pady=(0, 10))
        
        # Email
        ttk.Label(frame, text="Email:").pack(anchor='w', pady=2)
        self.entry_email = ttk.Entry(frame, width=50)
        self.entry_email.pack(fill='x', pady=(0, 10))
        
        # Justificativa
        ttk.Label(frame, text="Justificativa da requisição:").pack(anchor='w', pady=2)
        self.text_justificativa = scrolledtext.ScrolledText(frame, height=10, width=50, wrap=tk.WORD)
        self.text_justificativa.pack(fill='both', expand=True, pady=(0, 15))
        
        # Botões
        frame_botoes = ttk.Frame(frame)
        frame_botoes.pack(pady=10)
        
        ttk.Button(frame_botoes, text="Enviar Requisição", command=self._enviar).pack(side='left', padx=5)
        ttk.Button(frame_botoes, text="Cancelar", command=self.janela.destroy).pack(side='left', padx=5)
    
    def _enviar(self):
        """Envia a requisição"""
        nome = self.entry_nome.get().strip()
        email = self.entry_email.get().strip()
        justificativa = self.text_justificativa.get('1.0', 'end-1c').strip()
        
        try:
            self.ctr_requisicoes.criarRequisicao(nome, email, justificativa)
            messagebox.showinfo("Sucesso", 
                              "Requisição enviada com sucesso!\n"
                              "Aguarde a análise do administrador.")
            self.janela.destroy()
        
        except ValidationError as e:
            messagebox.showerror("Erro", str(e))
