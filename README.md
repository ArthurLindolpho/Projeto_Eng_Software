# Sistema de Monitoramento de Cães Domésticos

Sistema web para gerenciamento de dados de monitoramento de cães domésticos e fauna selvagem.

## Funcionalidades Implementadas

### 1. Gerenciar Permissões (CDU 2.3.2 - Administrador)
- **Gerenciar Usuários**: Visualizar, adicionar, editar e remover usuários do sistema
- **Recuperar Senha**: Resetar senha de usuários para o valor padrão (nome do usuário)
- **Gerenciar Requisições**: Visualizar, aceitar ou recusar requisições de acesso ao sistema
- **Filtros**: Buscar usuários e requisições por nome, email ou função

### 2. Cadastrar Cães Domésticos (CDU 2.3.6)
- **Visualizar Cães**: Listar todos os cães cadastrados com suas informações
- **Adicionar Cão**: Cadastrar novos cães no sistema
- **Editar Cão**: Atualizar informações de cães já cadastrados
- **Remover Cão**: Excluir cães do sistema
- **Filtros**: Buscar cães por nome, código ou status

## Tecnologias Utilizadas

- **Backend**: Python 3.x + Flask
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Armazenamento**: Em memória (dados de teste incluídos)
- **API**: REST API com JSON

## Estrutura do Projeto

\`\`\`
.
├── app.py                      # Servidor Flask e API REST
├── templates/
│   ├── index.html             # Página principal (menu)
│   ├── permissoes.html        # Gerenciamento de permissões
│   └── caes.html              # Cadastro de cães domésticos
├── static/
│   ├── css/
│   │   └── style.css          # Estilos globais
│   └── js/
│       ├── permissoes.js      # Lógica da página de permissões
│       └── caes.js            # Lógica da página de cães
├── requirements.txt            # Dependências Python
└── README.md                  # Este arquivo
\`\`\`

## Instalação

1. **Clone o repositório ou extraia os arquivos**

2. **Instale as dependências:**
\`\`\`bash
pip install -r requirements.txt
\`\`\`

## Executar o Sistema

1. **Inicie o servidor Flask:**
\`\`\`bash
python app.py
\`\`\`

2. **Acesse no navegador:**
\`\`\`
http://localhost:5000
\`\`\`

## Dados de Teste

O sistema vem pré-configurado com dados de teste:

### Usuários
- **Usuário A** (usu.a@exemplo.com) - Administrador
- **Usuário B** (usu.b@exemplo.com) - Legista
- **Usuário C** (usu.c@exemplo.com) - Veterinário

### Requisições
- **Usuário F** - Pesquisador de ectoparasitos
- **Usuário G** - Veterinário
- **Usuário H** - Pesquisador sorológico

### Cães
- **Rex** (cao-001) - Masculino, Ativo
- **Bella** (cao-002) - Feminino, Ativo
- **Max** (cao-003) - Masculino, Inativo

## Validações Implementadas

### Usuários
- ✅ Email em formato válido
- ✅ Verificação de duplicidade de email
- ✅ Todos os campos obrigatórios
- ✅ Senha inicial = nome do usuário

### Cães
- ✅ Todos os campos obrigatórios
- ✅ Data de nascimento no formato DD/MM/AAAA
- ✅ Sexo: Masculino ou Feminino
- ✅ Status: Ativo ou Inativo
- ✅ Código gerado automaticamente (formato: cao-XXX)

## API Endpoints

### Funções
- `GET /api/funcoes` - Lista todas as funções disponíveis

### Usuários
- `GET /api/usuarios` - Lista usuários (com filtros opcionais)
- `POST /api/usuarios` - Adiciona novo usuário
- `PUT /api/usuarios/<id>` - Atualiza usuário existente
- `DELETE /api/usuarios/<id>` - Remove usuário
- `POST /api/usuarios/<id>/recuperar-senha` - Recupera senha do usuário

### Requisições
- `GET /api/requisicoes` - Lista requisições (com filtros opcionais)
- `POST /api/requisicoes/<id>/aceitar` - Aceita requisição e cria usuário
- `POST /api/requisicoes/<id>/recusar` - Recusa e remove requisição

### Cães
- `GET /api/caes` - Lista cães (com filtros opcionais)
- `POST /api/caes` - Adiciona novo cão
- `PUT /api/caes/<id>` - Atualiza cão existente
- `DELETE /api/caes/<id>` - Remove cão

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
- **Breadcrumbs**: Indicação da página atual
- **Ações rápidas**: Botões de ação próximos aos dados

## Funções do Sistema

O sistema possui as seguintes funções/cargos disponíveis:
1. Administrador
2. Entrevistador
3. Veterinário
4. Legista
5. Pesquisador Sorológico

## Observações

- Os dados são armazenados em memória e serão perdidos ao reiniciar o servidor
- Para uso em produção, considere implementar persistência em banco de dados
- As interfaces foram desenvolvidas seguindo fielmente os designs fornecidos na documentação
- Seguindo rigorosamente os diagramas de classes de projeto e diagramas de comunicação

## Próximos Passos

Para expandir o sistema, considere implementar:
- Autenticação e login de usuários
- Persistência de dados em banco de dados (PostgreSQL, MySQL, etc.)
- Cadastro de tutores
- Sistema de entrevistas
- Rastreamento GPS
- Visitas veterinárias
- Exames e análises
- Registro de atropelamentos e necrópsias
