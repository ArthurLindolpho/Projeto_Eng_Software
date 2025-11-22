# Sistema de Monitoramento de Cães Domésticos

Sistema web para gerenciamento de dados de monitoramento de cães domésticos e fauna selvagem, desenvolvido para pesquisadores envolvidos no projeto de análise da relação entre cães domésticos e animais selvagens.

## Características

- **Autenticação e Autorização**: Sistema de login com diferentes níveis de acesso
- **Gerenciamento de Permissões**: Controle de usuários e requisições de acesso
- **Cadastro de Cães Domésticos**: Registro e acompanhamento de cães monitorados
- **Persistência de Dados**: Todos os dados são salvos automaticamente em arquivo JSON

## Funcionalidades Implementadas

### 1. Login e Requisição de Acesso
- Tela de login com validação de credenciais
- Página de requisição de acesso para novos usuários
- Recuperação de senha (reseta para o nome do usuário)

### 2. Gerenciar Permissões (CDU 2.3.2 - Administrador)

**Usuários:**
- Visualizar todos os usuários cadastrados
- Filtrar por nome, email ou função
- Adicionar novo usuário (senha inicial = nome completo)
- Editar informações de usuário
- Remover usuário (não permite remover a si mesmo)
- Recuperar senha de usuário

**Requisições:**
- Visualizar requisições pendentes
- Filtrar por nome ou email
- Expandir para ver justificativa completa
- Aceitar requisição (cria usuário com a senha escolhida)
- Recusar requisição
- Contador de requisições pendentes atualiza automaticamente

### 3. Cadastrar Cães Domésticos (CDU 2.3.6)
- Visualizar lista de cães cadastrados
- Filtrar por nome, código ou status
- Adicionar novo cão (código gerado automaticamente)
- Editar informações do cão
- Remover cão
- Campos: Nome, Data de Nascimento, Sexo (Masculino/Feminino), Status (Ativo/Inativo)

## Tecnologias Utilizadas

- **Backend**: Python 3.x com Flask
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Persistência**: Arquivo JSON (database.json)
- **Autenticação**: Flask Sessions

## Estrutura do Projeto

\`\`\`
.
├── app.py                  # Aplicação Flask principal
├── persistence.py          # Módulo de persistência de dados
├── models.py              # Classes de domínio (referência)
├── controllers.py         # Controladores (referência)
├── catalogs.py           # Catálogos (referência)
├── validations.py        # Validações (referência)
├── database.json         # Arquivo de dados persistidos (gerado automaticamente)
├── requirements.txt      # Dependências do projeto
├── templates/            # Templates HTML
│   ├── index.html
│   ├── login.html
│   ├── requisicao.html
│   ├── permissoes.html
│   └── caes.html
└── static/              # Arquivos estáticos
    ├── css/
    │   └── style.css
    └── js/
        ├── permissoes.js
        └── caes.js
\`\`\`

## Instalação

1. **Clone o repositório** (ou extraia o arquivo ZIP):
\`\`\`bash
cd sistema-monitoramento-caes
\`\`\`

2. **Instale as dependências**:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

3. **Execute o servidor**:
\`\`\`bash
python app.py
\`\`\`

4. **Acesse no navegador**:
\`\`\`
http://localhost:5000
\`\`\`

## Persistência de Dados

O sistema agora utiliza um arquivo `database.json` para persistir todos os dados entre reinicializações do servidor.

### Como Funciona

- **Carregamento Automático**: Ao iniciar o servidor, o sistema tenta carregar dados do arquivo `database.json`
- **Salvamento Automático**: Toda operação que modifica dados (adicionar, editar, remover) salva automaticamente no arquivo
- **Primeira Execução**: Se o arquivo não existir, o sistema cria dados padrão e salva automaticamente

### Gerenciamento de Dados

**Resetar para dados padrão** (remove dados personalizados):
\`\`\`bash
# Simplesmente delete o arquivo database.json e reinicie o servidor
rm database.json
python app.py
\`\`\`

**Fazer backup dos dados**:
\`\`\`bash
# Copie o arquivo database.json para um local seguro
cp database.json backup_database_$(date +%Y%m%d).json
\`\`\`

**Restaurar backup**:
\`\`\`bash
# Substitua o database.json pelo arquivo de backup
cp backup_database_YYYYMMDD.json database.json
\`\`\`

## Credenciais de Acesso Padrão

### Administradores
- Email: `natalie@exemplo.com` | Senha: `Natalie Olifiers`
- Email: `franciele@exemplo.com` | Senha: `Franciele Candito`
- Email: `usu.a@exemplo.com` | Senha: `Usuário A`

### Outros Usuários
- **Entrevistador**: `dantielly@exemplo.com` | Senha: `Dantielly Costa`
- **Veterinário**: `maisa@exemplo.com` | Senha: `Maisa Panzani`
- **Legista**: `usu.b@exemplo.com` | Senha: `Usuário B`
- **Veterinário**: `usu.c@exemplo.com` | Senha: `Usuário C`

## Validações Implementadas

### Email
- ✅ Formato válido de email
- ✅ Verificação de duplicidade no sistema
- ✅ Não permite emails já cadastrados ou em requisições pendentes

### Campos Obrigatórios
- ✅ Todos os campos de formulários são validados
- ✅ Mensagens de erro descritivas para o usuário

### Segurança
- ✅ Usuário não pode excluir a si mesmo
- ✅ Rotas protegidas por autenticação (decorator @login_required)
- ✅ Sessões seguras com chave secreta

## API Endpoints

### Autenticação
- `POST /login` - Realizar login
- `GET /logout` - Realizar logout
- `POST /requisicao-acesso` - Enviar requisição de acesso

### Usuários
- `GET /api/usuarios` - Listar usuários (com filtros opcionais)
- `POST /api/usuarios` - Adicionar novo usuário
- `PUT /api/usuarios/<id>` - Editar usuário
- `DELETE /api/usuarios/<id>` - Remover usuário
- `POST /api/usuarios/<id>/recuperar-senha` - Recuperar senha

### Requisições
- `GET /api/requisicoes` - Listar requisições (com filtros opcionais)
- `GET /api/requisicoes/count` - Contar requisições pendentes
- `POST /api/requisicoes/<id>/aceitar` - Aceitar requisição
- `POST /api/requisicoes/<id>/recusar` - Recusar requisição

### Cães
- `GET /api/caes` - Listar cães (com filtros opcionais)
- `POST /api/caes` - Adicionar novo cão
- `PUT /api/caes/<id>` - Editar cão
- `DELETE /api/caes/<id>` - Remover cão

### Funções
- `GET /api/funcoes` - Listar funções disponíveis

### Sessão
- `GET /api/sessao` - Obter dados do usuário logado

### Administração
- `POST /api/admin/salvar-dados` - Salvar dados manualmente
- `POST /api/admin/resetar-dados` - Resetar para dados padrão

## Níveis de Usuário

1. **Administrador** - Acesso total ao sistema
2. **Entrevistador** - Realiza entrevistas e cadastra tutores e cães
3. **Veterinário** - Registra visitas veterinárias
4. **Pesquisador Fezes** - Cadastra análises de fezes
5. **Pesquisador Vírus** - Registra resultados de exames de vírus
6. **Pesquisador Imunopatologia** - Registra resultados de imunopatologia
7. **Pesquisador Tripasomatídeos** - Registra resultados de tripasomatídeos
8. **Pesquisador Sorológico** - Registra análises sorológicas
9. **Pesquisador Ectoparasitos** - Cadastra análises de ectoparasitos
10. **Legista** - Registra atropelamentos e necrópsias
11. **Pesquisador Helmintos** - Cadastra análises de helmintos

## Interface do Usuário

### Design
- Layout responsivo com sidebar de navegação
- Cores e tipografia consistentes com a documentação
- Tabelas com ações inline
- Modais para formulários de edição
- Filtros em tempo real
- Feedback visual para ações do usuário

### Navegação
- **Menu lateral**: Acesso rápido a todas as funcionalidades
- **Abas**: Organização de conteúdo relacionado (Usuários/Requisições)
- **Ações rápidas**: Botões de ação próximos aos dados

## Solução de Problemas

**Problema: Os dados desaparecem ao reiniciar o servidor**
- Solução: Verifique se o arquivo `database.json` está sendo criado no mesmo diretório do `app.py`
- Verifique as permissões de escrita no diretório

**Problema: Não consigo fazer login**
- Verifique se está usando as credenciais corretas (email e senha exatos)
- Tente resetar os dados deletando o `database.json` e reiniciando o servidor

**Problema: Erro ao salvar dados**
- Verifique as permissões de escrita no diretório
- Verifique se há espaço em disco disponível

**Problema: Contador de requisições não atualiza**
- Isso foi corrigido! O contador agora atualiza automaticamente após aceitar/recusar requisições

## Desenvolvimento

O sistema foi desenvolvido seguindo os diagramas de casos de uso, classes e comunicação fornecidos na documentação do projeto.

### Casos de Uso Implementados
- 2.3.2 - Gerenciar permissões
- 2.3.6 - Cadastrar cão doméstico

## Equipe

**Grupo 10 (G10):**
- Arthur Tavares
- Mateus Arthur
- Nícolas Ouverney

**Coordenadores do Projeto:**
- Dra. Natalie Olifiers
- Mestra Franciele Candito

