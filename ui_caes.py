"""
Interface gráfica para cadastro de cães domésticos
"""
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from controllers import CTRCaesDom
from validations import ValidationError


class UICaesDom:
    """Interface para cadastro de cães domésticos"""
    
    def __init__(self, root: tk.Tk, ctr_caes: CTRCaesDom):
        self.root = root
        self.ctr_caes = ctr_caes
        
        # Configuração da janela
        self.root.title("Sistema de Monitoramento - Cães Domésticos")
        self.root.geometry("1200x700")
        
        # Frame principal
        frame_main = ttk.Frame(root)
        frame_main.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Título
        ttk.Label(frame_main, text="CÃES DOMÉSTICOS", font=('Arial', 16, 'bold')).pack(pady=10)
        
        # Frame superior - Filtros e adicionar
        frame_top = ttk.Frame(frame_main)
        frame_top.pack(fill='x', padx=10, pady=10)
        
        ttk.Label(frame_top, text="Filtrar:", font=('Arial', 10, 'bold')).pack(side='left', padx=5)
        
        self.filtro_tipo = ttk.Combobox(frame_top, values=['nome', 'codigo', 'status'], 
                                        width=10, state='readonly')
        self.filtro_tipo.set('nome')
        self.filtro_tipo.pack(side='left', padx=5)
        
        self.filtro_termo = ttk.Entry(frame_top, width=30)
        self.filtro_termo.pack(side='left', padx=5)
        
        ttk.Button(frame_top, text="Filtrar", command=self._filtrar_caes).pack(side='left', padx=5)
        ttk.Button(frame_top, text="Limpar", command=self._carregar_caes).pack(side='left', padx=5)
        
        ttk.Button(frame_top, text="+ Adicionar Cão", command=self._abrir_form_adicionar).pack(side='right', padx=5)
        
        # Frame da tabela
        frame_tabela = ttk.Frame(frame_main)
        frame_tabela.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(frame_tabela)
        scrollbar.pack(side='right', fill='y')
        
        # Treeview
        colunas = ('Código', 'Nome', 'Data Nasc', 'Sexo', 'Status')
        self.tree_caes = ttk.Treeview(frame_tabela, columns=colunas, show='headings',
                                      yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree_caes.yview)
        
        # Configurar colunas
        self.tree_caes.heading('Código', text='Código (ID)')
        self.tree_caes.heading('Nome', text='Nome')
        self.tree_caes.heading('Data Nasc', text='Data de Nascimento')
        self.tree_caes.heading('Sexo', text='Sexo')
        self.tree_caes.heading('Status', text='Status')
        
        self.tree_caes.column('Código', width=100)
        self.tree_caes.column('Nome', width=250)
        self.tree_caes.column('Data Nasc', width=200)
        self.tree_caes.column('Sexo', width=150)
        self.tree_caes.column('Status', width=150)
        
        self.tree_caes.pack(fill='both', expand=True)
        
        # Duplo clique para expandir
        self.tree_caes.bind('<Double-1>', lambda e: self._expandir_cao())
        
        # Frame inferior - Ações
        frame_acoes = ttk.Frame(frame_main)
        frame_acoes.pack(fill='x', padx=10, pady=10)
        
        ttk.Button(frame_acoes, text="Expandir", command=self._expandir_cao).pack(side='left', padx=5)
        ttk.Button(frame_acoes, text="Editar", command=self._editar_cao).pack(side='left', padx=5)
        ttk.Button(frame_acoes, text="Remover", command=self._remover_cao).pack(side='left', padx=5)
        
        # Carregar dados
        self._carregar_caes()
    
    def _carregar_caes(self):
        """Carrega lista de cães na tabela"""
        # Limpar tabela
        for item in self.tree_caes.get_children():
            self.tree_caes.delete(item)
        
        # Carregar dados
        caes = self.ctr_caes.visualizarListaCaes()
        for cao in caes:
            self.tree_caes.insert('', 'end', values=(
                cao['idCao'],
                cao['nome'],
                cao['dataNasc'],
                cao['sexo'],
                cao['status']
            ))
    
    def _filtrar_caes(self):
        """Filtra cães"""
        tipo = self.filtro_tipo.get()
        termo = self.filtro_termo.get()
        
        if not termo:
            self._carregar_caes()
            return
        
        # Limpar tabela
        for item in self.tree_caes.get_children():
            self.tree_caes.delete(item)
        
        # Carregar dados filtrados
        caes = self.ctr_caes.filtrarListaCaes(tipo, termo)
        for cao in caes:
            self.tree_caes.insert('', 'end', values=(
                cao['idCao'],
                cao['nome'],
                cao['dataNasc'],
                cao['sexo'],
                cao['status']
            ))
    
    def _expandir_cao(self):
        """Expande detalhes do cão selecionado"""
        selecionado = self.tree_caes.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um cão para expandir")
            return
        
        item = self.tree_caes.item(selecionado[0])
        id_cao = item['values'][0]
        
        try:
            cao = self.ctr_caes.expandir(id_cao)
            
            # Janela de detalhes
            janela = tk.Toplevel(self.root)
            janela.title(f"Detalhes do Cão - {cao['nome']}")
            janela.geometry("500x350")
            
            ttk.Label(janela, text="INFORMAÇÕES DO CÃO", font=('Arial', 12, 'bold')).pack(pady=10)
            
            frame_info = ttk.Frame(janela, padding=20)
            frame_info.pack(fill='both', expand=True)
            
            ttk.Label(frame_info, text=f"Código (ID): {cao['idCao']}", font=('Arial', 10)).pack(anchor='w', pady=5)
            ttk.Label(frame_info, text=f"Nome: {cao['nome']}", font=('Arial', 10)).pack(anchor='w', pady=5)
            ttk.Label(frame_info, text=f"Data de Nascimento: {cao['dataNasc']}", font=('Arial', 10)).pack(anchor='w', pady=5)
            ttk.Label(frame_info, text=f"Sexo: {cao['sexo']}", font=('Arial', 10)).pack(anchor='w', pady=5)
            ttk.Label(frame_info, text=f"Status: {cao['status']}", font=('Arial', 10)).pack(anchor='w', pady=5)
            
        except ValidationError as e:
            messagebox.showerror("Erro", str(e))
    
    def _abrir_form_adicionar(self):
        """Abre formulário para adicionar cão"""
        FormCao(self.root, self.ctr_caes, callback=self._carregar_caes)
    
    def _editar_cao(self):
        """Edita cão selecionado"""
        selecionado = self.tree_caes.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um cão para editar")
            return
        
        item = self.tree_caes.item(selecionado[0])
        id_cao = item['values'][0]
        
        FormCao(self.root, self.ctr_caes, id_cao=id_cao, callback=self._carregar_caes)
    
    def _remover_cao(self):
        """Remove cão selecionado"""
        selecionado = self.tree_caes.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um cão para remover")
            return
        
        item = self.tree_caes.item(selecionado[0])
        id_cao = item['values'][0]
        nome = item['values'][1]
        
        if messagebox.askyesno("Confirmar", f"Deseja realmente remover o cão '{nome}'?"):
            try:
                self.ctr_caes.removerCao(id_cao)
                messagebox.showinfo("Sucesso", "Cão removido com sucesso!")
                self._carregar_caes()
            except ValidationError as e:
                messagebox.showerror("Erro", str(e))


class FormCao:
    """Formulário para adicionar/editar cão"""
    
    def __init__(self, parent, ctr_caes: CTRCaesDom, id_cao=None, callback=None):
        self.ctr_caes = ctr_caes
        self.id_cao = id_cao
        self.callback = callback
        
        # Janela
        self.janela = tk.Toplevel(parent)
        self.janela.title("Adicionar Cão" if id_cao is None else "Editar Cão")
        self.janela.geometry("450x350")
        self.janela.transient(parent)
        self.janela.grab_set()
        
        # Frame principal
        frame = ttk.Frame(self.janela, padding=20)
        frame.pack(fill='both', expand=True)
        
        # Nome
        ttk.Label(frame, text="Nome:").grid(row=0, column=0, sticky='w', pady=5)
        self.entry_nome = ttk.Entry(frame, width=35)
        self.entry_nome.grid(row=0, column=1, pady=5)
        
        # Data de Nascimento
        ttk.Label(frame, text="Data de Nascimento:").grid(row=1, column=0, sticky='w', pady=5)
        self.entry_data = DateEntry(frame, width=32, date_pattern='dd/mm/yyyy')
        self.entry_data.grid(row=1, column=1, pady=5)
        
        # Sexo
        ttk.Label(frame, text="Sexo:").grid(row=2, column=0, sticky='w', pady=5)
        self.combo_sexo = ttk.Combobox(frame, values=['Masculino', 'Feminino'], 
                                       width=32, state='readonly')
        self.combo_sexo.grid(row=2, column=1, pady=5)
        
        # Status
        ttk.Label(frame, text="Status:").grid(row=3, column=0, sticky='w', pady=5)
        self.combo_status = ttk.Combobox(frame, values=['Ativo', 'Inativo'],
                                         width=32, state='readonly')
        self.combo_status.grid(row=3, column=1, pady=5)
        
        
        # Se for edição, carregar dados
        if id_cao is not None:
            self._carregar_dados()
        
        # Botões
        frame_botoes = ttk.Frame(frame)
        frame_botoes.grid(row=4, column=0, columnspan=2, pady=20)
        
        ttk.Button(frame_botoes, text="Salvar", command=self._salvar).pack(side='left', padx=5)
        ttk.Button(frame_botoes, text="Cancelar", command=self.janela.destroy).pack(side='left', padx=5)
    
    def _carregar_dados(self):
        """Carrega dados do cão para edição"""
        cao = self.ctr_caes.cat_caes.encontrarCao(self.id_cao)
        if cao:
            self.entry_nome.insert(0, cao.nome)
            # Converte data de string para o DateEntry
            from datetime import datetime
            try:
                data_obj = datetime.strptime(cao.dataNasc, '%d/%m/%Y')
                self.entry_data.set_date(data_obj)
            except:
                pass
            self.combo_sexo.set(cao.sexo)
            self.combo_status.set(cao.status)
    
    def _salvar(self):
        """Salva cão"""
        nome = self.entry_nome.get().strip()
        data_nasc = self.entry_data.get()
        sexo = self.combo_sexo.get()
        status = self.combo_status.get()
        
        
        try:
            if self.id_cao is None:
                # Adicionar novo
                self.ctr_caes.adicionarCao(nome, data_nasc, sexo, status)
                messagebox.showinfo("Sucesso", "Cão cadastrado com sucesso!")
            else:
                # Editar existente
                self.ctr_caes.editarCao(self.id_cao, nome, data_nasc, sexo, status)
                messagebox.showinfo("Sucesso", "Cão atualizado com sucesso!")
            
            if self.callback:
                self.callback()
            
            self.janela.destroy()
        
        except ValidationError as e:
            messagebox.showerror("Erro", str(e))
