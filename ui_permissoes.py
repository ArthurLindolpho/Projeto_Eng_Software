"""
Interface gráfica para gerenciamento de permissões
Implementa as telas de usuários e requisições
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from controllers import CTRUsuarios, CTRRequisicoes
from validations import ValidationError


class UIPermissoes:
    """Interface para gerenciamento de permissões"""
    
    def __init__(self, root: tk.Tk, ctr_usuarios: CTRUsuarios, ctr_requisicoes: CTRRequisicoes):
        self.root = root
        self.ctr_usuarios = ctr_usuarios
        self.ctr_requisicoes = ctr_requisicoes
        
        # Configuração da janela principal
        self.root.title("Sistema de Monitoramento - Gerenciar Permissões")
        self.root.geometry("1200x700")
        
        # Notebook para abas
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Aba de Usuários
        self.frame_usuarios = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_usuarios, text="Usuários")
        self._criar_interface_usuarios()
        
        # Aba de Requisições
        self.frame_requisicoes = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_requisicoes, text="Requisições")
        self._criar_interface_requisicoes()
    
    def _criar_interface_usuarios(self):
        """Cria interface da aba de usuários"""
        # Frame superior - Filtros e adicionar
        frame_top = ttk.Frame(self.frame_usuarios)
        frame_top.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(frame_top, text="Filtrar:", font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        
        self.filtro_tipo_usu = ttk.Combobox(frame_top, values=['nome', 'email'], width=10, state='readonly')
        self.filtro_tipo_usu.set('nome')
        self.filtro_tipo_usu.pack(side='left', padx=5)
        
        self.filtro_termo_usu = ttk.Entry(frame_top, width=30)
        self.filtro_termo_usu.pack(side='left', padx=5)
        
        ttk.Button(frame_top, text="Filtrar", command=self._filtrar_usuarios).pack(side='left', padx=5)
        ttk.Button(frame_top, text="Limpar", command=self._carregar_usuarios).pack(side='left', padx=5)
        
        ttk.Button(frame_top, text="+ Adicionar Usuário", command=self._abrir_form_adicionar_usuario).pack(side='right', padx=5)
        
        # Frame da tabela
        frame_tabela = ttk.Frame(self.frame_usuarios)
        frame_tabela.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabela)
        scrollbar.pack(side='right', fill='y')
        
        # Treeview
        colunas = ('ID', 'Nome', 'Email', 'Função')
        self.tree_usuarios = ttk.Treeview(frame_tabela, columns=colunas, show='headings', 
                                          yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree_usuarios.yview)
        
        # Configurar colunas
        self.tree_usuarios.heading('ID', text='ID')
        self.tree_usuarios.heading('Nome', text='Nome')
        self.tree_usuarios.heading('Email', text='Email')
        self.tree_usuarios.heading('Função', text='Função')
        
        self.tree_usuarios.column('ID', width=50)
        self.tree_usuarios.column('Nome', width=250)
        self.tree_usuarios.column('Email', width=250)
        self.tree_usuarios.column('Função', width=200)
        
        self.tree_usuarios.pack(fill='both', expand=True)
        
        # Frame inferior - Ações
        frame_acoes = ttk.Frame(self.frame_usuarios)
        frame_acoes.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(frame_acoes, text="Editar", command=self._editar_usuario).pack(side='left', padx=5)
        ttk.Button(frame_acoes, text="Remover", command=self._remover_usuario).pack(side='left', padx=5)
        ttk.Button(frame_acoes, text="Recuperar Senha", command=self._recuperar_senha).pack(side='left', padx=5)
        
        # Carregar dados
        self._carregar_usuarios()
    
    def _criar_interface_requisicoes(self):
        """Cria interface da aba de requisições"""
        # Frame superior - Filtros
        frame_top = ttk.Frame(self.frame_requisicoes)
        frame_top.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(frame_top, text="Filtrar:", font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        
        self.filtro_tipo_req = ttk.Combobox(frame_top, values=['nome', 'email'], width=10, state='readonly')
        self.filtro_tipo_req.set('nome')
        self.filtro_tipo_req.pack(side='left', padx=5)
        
        self.filtro_termo_req = ttk.Entry(frame_top, width=30)
        self.filtro_termo_req.pack(side='left', padx=5)
        
        ttk.Button(frame_top, text="Filtrar", command=self._filtrar_requisicoes).pack(side='left', padx=5)
        ttk.Button(frame_top, text="Limpar", command=self._carregar_requisicoes).pack(side='left', padx=5)
        
        # Frame da tabela
        frame_tabela = ttk.Frame(self.frame_requisicoes)
        frame_tabela.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabela)
        scrollbar.pack(side='right', fill='y')
        
        # Treeview
        colunas = ('ID', 'Nome', 'Email', 'Data')
        self.tree_requisicoes = ttk.Treeview(frame_tabela, columns=colunas, show='headings',
                                             yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree_requisicoes.yview)
        
        # Configurar colunas
        self.tree_requisicoes.heading('ID', text='ID')
        self.tree_requisicoes.heading('Nome', text='Nome')
        self.tree_requisicoes.heading('Email', text='Email')
        self.tree_requisicoes.heading('Data', text='Data')
        
        self.tree_requisicoes.column('ID', width=50)
        self.tree_requisicoes.column('Nome', width=250)
        self.tree_requisicoes.column('Email', width=250)
        self.tree_requisicoes.column('Data', width=100)
        
        self.tree_requisicoes.pack(fill='both', expand=True)
        
        # Frame inferior - Ações
        frame_acoes = ttk.Frame(self.frame_requisicoes)
        frame_acoes.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(frame_acoes, text="Expandir", command=self._expandir_requisicao).pack(side='left', padx=5)
        ttk.Button(frame_acoes, text="Aceitar", command=self._aceitar_requisicao).pack(side='left', padx=5)
        ttk.Button(frame_acoes, text="Recusar", command=self._recusar_requisicao).pack(side='left', padx=5)
        
        # Carregar dados
        self._carregar_requisicoes()
    
    def _carregar_usuarios(self):
        """Carrega lista de usuários na tabela"""
        # Limpar tabela
        for item in self.tree_usuarios.get_children():
            self.tree_usuarios.delete(item)
        
        # Carregar dados
        usuarios = self.ctr_usuarios.visualizarListaUsu()
        for usuario in usuarios:
            self.tree_usuarios.insert('', 'end', values=(
                usuario['idUsu'],
                usuario['nome'],
                usuario['email'],
                usuario['funcao']
            ))
    
    def _filtrar_usuarios(self):
        """Filtra usuários"""
        tipo = self.filtro_tipo_usu.get()
        termo = self.filtro_termo_usu.get()
        
        if not termo:
            self._carregar_usuarios()
            return
        
        # Limpar tabela
        for item in self.tree_usuarios.get_children():
            self.tree_usuarios.delete(item)
        
        # Carregar dados filtrados
        usuarios = self.ctr_usuarios.filtrarListaUsu(tipo, termo)
        for usuario in usuarios:
            self.tree_usuarios.insert('', 'end', values=(
                usuario['idUsu'],
                usuario['nome'],
                usuario['email'],
                usuario['funcao']
            ))
    
    def _abrir_form_adicionar_usuario(self):
        """Abre formulário para adicionar usuário"""
        FormUsuario(self.root, self.ctr_usuarios, callback=self._carregar_usuarios)
    
    def _editar_usuario(self):
        """Edita usuário selecionado"""
        selecionado = self.tree_usuarios.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um usuário para editar")
            return
        
        item = self.tree_usuarios.item(selecionado[0])
        id_usuario = item['values'][0]
        
        FormUsuario(self.root, self.ctr_usuarios, id_usuario=id_usuario, callback=self._carregar_usuarios)
    
    def _remover_usuario(self):
        """Remove usuário selecionado"""
        selecionado = self.tree_usuarios.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um usuário para remover")
            return
        
        item = self.tree_usuarios.item(selecionado[0])
        id_usuario = item['values'][0]
        nome = item['values'][1]
        
        if messagebox.askyesno("Confirmar", f"Deseja realmente remover o usuário '{nome}'?"):
            try:
                self.ctr_usuarios.removerUsu(id_usuario)
                messagebox.showinfo("Sucesso", "Usuário removido com sucesso!")
                self._carregar_usuarios()
            except ValidationError as e:
                messagebox.showerror("Erro", str(e))
    
    def _recuperar_senha(self):
        """Recupera senha do usuário selecionado"""
        selecionado = self.tree_usuarios.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um usuário para recuperar a senha")
            return
        
        item = self.tree_usuarios.item(selecionado[0])
        id_usuario = item['values'][0]
        nome = item['values'][1]
        
        if messagebox.askyesno("Confirmar", f"Recuperar senha do usuário '{nome}'?\nA nova senha será o nome completo do usuário."):
            try:
                self.ctr_usuarios.recuperarSenha(id_usuario)
                messagebox.showinfo("Sucesso", f"Senha recuperada com sucesso!\nNova senha: {nome}")
            except ValidationError as e:
                messagebox.showerror("Erro", str(e))
    
    def _carregar_requisicoes(self):
        """Carrega lista de requisições na tabela"""
        # Limpar tabela
        for item in self.tree_requisicoes.get_children():
            self.tree_requisicoes.delete(item)
        
        # Carregar dados
        requisicoes = self.ctr_requisicoes.visualizarListaReq()
        for req in requisicoes:
            self.tree_requisicoes.insert('', 'end', values=(
                req['idReq'],
                req['nome'],
                req['email'],
                req['data']
            ))
    
    def _filtrar_requisicoes(self):
        """Filtra requisições"""
        tipo = self.filtro_tipo_req.get()
        termo = self.filtro_termo_req.get()
        
        if not termo:
            self._carregar_requisicoes()
            return
        
        # Limpar tabela
        for item in self.tree_requisicoes.get_children():
            self.tree_requisicoes.delete(item)
        
        # Carregar dados filtrados
        requisicoes = self.ctr_requisicoes.filtrarListaReq(tipo, termo)
        for req in requisicoes:
            self.tree_requisicoes.insert('', 'end', values=(
                req['idReq'],
                req['nome'],
                req['email'],
                req['data']
            ))
    
    def _expandir_requisicao(self):
        """Expande detalhes da requisição selecionada"""
        selecionado = self.tree_requisicoes.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma requisição para expandir")
            return
        
        item = self.tree_requisicoes.item(selecionado[0])
        id_req = item['values'][0]
        
        try:
            req = self.ctr_requisicoes.expandir(id_req)
            
            # Janela de detalhes
            janela = tk.Toplevel(self.root)
            janela.title("Detalhes da Requisição")
            janela.geometry("500x400")
            
            ttk.Label(janela, text="INFORMAÇÕES DA REQUISIÇÃO", font=('Arial', 12, 'bold')).pack(pady=10)
            
            frame_info = ttk.Frame(janela)
            frame_info.pack(fill='both', expand=True, padx=20, pady=10)
            
            ttk.Label(frame_info, text=f"ID: {req['idReq']}", font=('Arial', 10)).pack(anchor='w', pady=5)
            ttk.Label(frame_info, text=f"Nome: {req['nome']}", font=('Arial', 10)).pack(anchor='w', pady=5)
            ttk.Label(frame_info, text=f"Email: {req['email']}", font=('Arial', 10)).pack(anchor='w', pady=5)
            ttk.Label(frame_info, text=f"Data: {req['data']}", font=('Arial', 10)).pack(anchor='w', pady=5)
            
            ttk.Label(frame_info, text="Justificativa:", font=('Arial', 10, 'bold')).pack(anchor='w', pady=(15, 5))
            
            text_justificativa = scrolledtext.ScrolledText(frame_info, height=8, width=50, wrap=tk.WORD)
            text_justificativa.insert('1.0', req['justificativa'])
            text_justificativa.config(state='disabled')
            text_justificativa.pack(fill='both', expand=True)
            
        except ValidationError as e:
            messagebox.showerror("Erro", str(e))
    
    def _aceitar_requisicao(self):
        """Aceita requisição selecionada"""
        selecionado = self.tree_requisicoes.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma requisição para aceitar")
            return
        
        item = self.tree_requisicoes.item(selecionado[0])
        id_req = item['values'][0]
        nome = item['values'][1]
        
        # Janela para selecionar função
        FormAceitarRequisicao(self.root, self.ctr_requisicoes, id_req, nome, 
                              callback=self._carregar_requisicoes)
    
    def _recusar_requisicao(self):
        """Recusa requisição selecionada"""
        selecionado = self.tree_requisicoes.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma requisição para recusar")
            return
        
        item = self.tree_requisicoes.item(selecionado[0])
        id_req = item['values'][0]
        nome = item['values'][1]
        
        if messagebox.askyesno("Confirmar", f"Deseja realmente recusar a requisição de '{nome}'?"):
            try:
                self.ctr_requisicoes.recusarReq(id_req)
                messagebox.showinfo("Sucesso", "Requisição recusada!")
                self._carregar_requisicoes()
            except ValidationError as e:
                messagebox.showerror("Erro", str(e))


class FormUsuario:
    """Formulário para adicionar/editar usuário"""
    
    def __init__(self, parent, ctr_usuarios: CTRUsuarios, id_usuario=None, callback=None):
        self.ctr_usuarios = ctr_usuarios
        self.id_usuario = id_usuario
        self.callback = callback
        
        # Janela
        self.janela = tk.Toplevel(parent)
        self.janela.title("Adicionar Usuário" if id_usuario is None else "Editar Usuário")
        self.janela.geometry("450x300")
        self.janela.transient(parent)
        self.janela.grab_set()
        
        # Frame principal
        frame = ttk.Frame(self.janela, padding=20)
        frame.pack(fill='both', expand=True)
        
        # Nome
        ttk.Label(frame, text="Nome Completo:").grid(row=0, column=0, sticky='w', pady=5)
        self.entry_nome = ttk.Entry(frame, width=40)
        self.entry_nome.grid(row=0, column=1, pady=5)
        
        # Email
        ttk.Label(frame, text="Email:").grid(row=1, column=0, sticky='w', pady=5)
        self.entry_email = ttk.Entry(frame, width=40)
        self.entry_email.grid(row=1, column=1, pady=5)
        
        # Função
        ttk.Label(frame, text="Função:").grid(row=2, column=0, sticky='w', pady=5)
        
        funcoes = self.ctr_usuarios.cat_funcoes.listar_todas()
        self.funcoes_map = {f"{f.nome}": f.idFuncao for f in funcoes}
        
        self.combo_funcao = ttk.Combobox(frame, values=list(self.funcoes_map.keys()), 
                                         width=37, state='readonly')
        self.combo_funcao.grid(row=2, column=1, pady=5)
        
        # Se for edição, carregar dados
        if id_usuario is not None:
            self._carregar_dados()
        
        # Botões
        frame_botoes = ttk.Frame(frame)
        frame_botoes.grid(row=3, column=0, columnspan=2, pady=20)
        
        ttk.Button(frame_botoes, text="Salvar", command=self._salvar).pack(side='left', padx=5)
        ttk.Button(frame_botoes, text="Cancelar", command=self.janela.destroy).pack(side='left', padx=5)
    
    def _carregar_dados(self):
        """Carrega dados do usuário para edição"""
        usuario = self.ctr_usuarios.cat_usuarios.encontrarUsu(self.id_usuario)
        if usuario:
            self.entry_nome.insert(0, usuario.nome)
            self.entry_email.insert(0, usuario.email)
            self.combo_funcao.set(usuario.funcao.nome)
    
    def _salvar(self):
        """Salva usuário"""
        nome = self.entry_nome.get().strip()
        email = self.entry_email.get().strip()
        funcao_nome = self.combo_funcao.get()
        
        if not funcao_nome:
            messagebox.showerror("Erro", "Selecione uma função")
            return
        
        id_funcao = self.funcoes_map[funcao_nome]
        
        try:
            if self.id_usuario is None:
                # Adicionar novo
                self.ctr_usuarios.adicionarUsu(nome, email, id_funcao)
                messagebox.showinfo("Sucesso", f"Usuário cadastrado com sucesso!\nSenha inicial: {nome}")
            else:
                # Editar existente
                self.ctr_usuarios.editarUsu(self.id_usuario, nome, email, id_funcao)
                messagebox.showinfo("Sucesso", "Usuário atualizado com sucesso!")
            
            if self.callback:
                self.callback()
            
            self.janela.destroy()
        
        except ValidationError as e:
            messagebox.showerror("Erro", str(e))


class FormAceitarRequisicao:
    """Formulário para aceitar requisição"""
    
    def __init__(self, parent, ctr_requisicoes: CTRRequisicoes, id_req: int, 
                 nome_requerente: str, callback=None):
        self.ctr_requisicoes = ctr_requisicoes
        self.id_req = id_req
        self.callback = callback
        
        # Janela
        self.janela = tk.Toplevel(parent)
        self.janela.title(f"Aceitar Requisição - {nome_requerente}")
        self.janela.geometry("400x200")
        self.janela.transient(parent)
        self.janela.grab_set()
        
        # Frame principal
        frame = ttk.Frame(self.janela, padding=20)
        frame.pack(fill='both', expand=True)
        
        ttk.Label(frame, text="Selecione a função para o novo usuário:", 
                  font=('Arial', 10, 'bold')).pack(pady=10)
        
        # Função
        funcoes = self.ctr_requisicoes.cat_funcoes.listar_todas()
        self.funcoes_map = {f"{f.nome}": f.idFuncao for f in funcoes}
        
        self.combo_funcao = ttk.Combobox(frame, values=list(self.funcoes_map.keys()),
                                         width=35, state='readonly')
        self.combo_funcao.pack(pady=10)
        
        # Botões
        frame_botoes = ttk.Frame(frame)
        frame_botoes.pack(pady=20)
        
        ttk.Button(frame_botoes, text="Aceitar", command=self._aceitar).pack(side='left', padx=5)
        ttk.Button(frame_botoes, text="Cancelar", command=self.janela.destroy).pack(side='left', padx=5)
    
    def _aceitar(self):
        """Aceita a requisição"""
        funcao_nome = self.combo_funcao.get()
        
        if not funcao_nome:
            messagebox.showerror("Erro", "Selecione uma função")
            return
        
        id_funcao = self.funcoes_map[funcao_nome]
        
        try:
            self.ctr_requisicoes.aceitarReq(self.id_req, id_funcao)
            messagebox.showinfo("Sucesso", "Requisição aceita! Usuário criado com sucesso.")
            
            if self.callback:
                self.callback()
            
            self.janela.destroy()
        
        except ValidationError as e:
            messagebox.showerror("Erro", str(e))
