let funcoes = [];
let usuarios = [];
let requisicoes = [];

// Carregar dados iniciais
window.addEventListener('DOMContentLoaded', () => {
    carregarFuncoes();
    carregarUsuarios();
    carregarRequisicoes();
});

// Tabs
function openTab(tabName) {
    const tabs = document.querySelectorAll('.tab-content');
    tabs.forEach(tab => tab.classList.remove('active'));
    
    const buttons = document.querySelectorAll('.tab-button');
    buttons.forEach(btn => btn.classList.remove('active'));
    
    document.getElementById(tabName).classList.add('active');
    event.target.classList.add('active');
}

// Carregar funções
async function carregarFuncoes() {
    try {
        const response = await fetch('/api/funcoes');
        funcoes = await response.json();
        
        // Preencher selects
        const selectNova = document.getElementById('novaFuncao');
        const selectEditar = document.getElementById('editarFuncao');
        
        funcoes.forEach(funcao => {
            const option1 = new Option(funcao.nome, funcao.idFuncao);
            const option2 = new Option(funcao.nome, funcao.idFuncao);
            selectNova.add(option1);
            selectEditar.add(option2);
        });
    } catch (error) {
        console.error('Erro ao carregar funções:', error);
    }
}

// Carregar usuários
async function carregarUsuarios() {
    try {
        const tipo = document.getElementById('filtroTipoUsuario').value;
        const termo = document.getElementById('filtroTermoUsuario').value;
        
        let url = '/api/usuarios';
        if (tipo && termo) {
            url += `?tipo=${tipo}&termo=${encodeURIComponent(termo)}`;
        }
        
        const response = await fetch(url);
        usuarios = await response.json();
        renderizarUsuarios();
    } catch (error) {
        console.error('Erro ao carregar usuários:', error);
    }
}

function renderizarUsuarios() {
    const tbody = document.getElementById('tabelaUsuarios');
    tbody.innerHTML = '';
    
    usuarios.forEach(usuario => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${usuario.nome}</td>
            <td>${usuario.email}</td>
            <td>${usuario.funcao.nome}</td>
            <td>
                <button class="action-btn edit" onclick="abrirModalEditar(${usuario.idUsu})">Editar</button>
                <button class="action-btn delete" onclick="removerUsuario(${usuario.idUsu})">Remover</button>
                <button class="action-btn recover" onclick="recuperarSenha(${usuario.idUsu})">Recuperar Senha</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

function filtrarUsuarios() {
    carregarUsuarios();
}

function limparFiltroUsuarios() {
    document.getElementById('filtroTermoUsuario').value = '';
    carregarUsuarios();
}

// Adicionar usuário
async function adicionarUsuario() {
    const nome = document.getElementById('novoNome').value;
    const email = document.getElementById('novoEmail').value;
    const idFuncao = parseInt(document.getElementById('novaFuncao').value);
    
    if (!nome || !email || !idFuncao) {
        alert('Todos os campos são obrigatórios!');
        return;
    }
    
    try {
        const response = await fetch('/api/usuarios', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ nome, email, idFuncao })
        });
        
        if (response.ok) {
            alert('Usuário adicionado com sucesso!');
            document.getElementById('novoNome').value = '';
            document.getElementById('novoEmail').value = '';
            document.getElementById('novaFuncao').value = '';
            carregarUsuarios();
        } else {
            const error = await response.json();
            alert('Erro: ' + error.erro);
        }
    } catch (error) {
        console.error('Erro ao adicionar usuário:', error);
        alert('Erro ao adicionar usuário');
    }
}

// Editar usuário
function abrirModalEditar(idUsu) {
    const usuario = usuarios.find(u => u.idUsu === idUsu);
    if (!usuario) return;
    
    document.getElementById('editarIdUsu').value = usuario.idUsu;
    document.getElementById('editarNome').value = usuario.nome;
    document.getElementById('editarEmail').value = usuario.email;
    document.getElementById('editarFuncao').value = usuario.funcao.idFuncao;
    
    document.getElementById('modalEditarUsuario').style.display = 'block';
}

function fecharModalEditar() {
    document.getElementById('modalEditarUsuario').style.display = 'none';
}

async function salvarEdicaoUsuario() {
    const idUsu = parseInt(document.getElementById('editarIdUsu').value);
    const nome = document.getElementById('editarNome').value;
    const email = document.getElementById('editarEmail').value;
    const idFuncao = parseInt(document.getElementById('editarFuncao').value);
    
    if (!nome || !email || !idFuncao) {
        alert('Todos os campos são obrigatórios!');
        return;
    }
    
    try {
        const response = await fetch(`/api/usuarios/${idUsu}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ nome, email, idFuncao })
        });
        
        if (response.ok) {
            alert('Usuário atualizado com sucesso!');
            fecharModalEditar();
            carregarUsuarios();
        } else {
            const error = await response.json();
            alert('Erro: ' + error.erro);
        }
    } catch (error) {
        console.error('Erro ao editar usuário:', error);
        alert('Erro ao editar usuário');
    }
}

// Remover usuário
async function removerUsuario(idUsu) {
    if (!confirm('Tem certeza que deseja remover este usuário?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/usuarios/${idUsu}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            alert('Usuário removido com sucesso!');
            carregarUsuarios();
        } else {
            const error = await response.json();
            alert('Erro: ' + error.erro);
        }
    } catch (error) {
        console.error('Erro ao remover usuário:', error);
        alert('Erro ao remover usuário');
    }
}

// Recuperar senha
async function recuperarSenha(idUsu) {
    if (!confirm('Tem certeza que deseja recuperar a senha deste usuário?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/usuarios/${idUsu}/recuperar-senha`, {
            method: 'POST'
        });
        
        if (response.ok) {
            const data = await response.json();
            alert(`Senha recuperada com sucesso!\nNova senha: ${data.nova_senha}`);
        } else {
            const error = await response.json();
            alert('Erro: ' + error.erro);
        }
    } catch (error) {
        console.error('Erro ao recuperar senha:', error);
        alert('Erro ao recuperar senha');
    }
}

// Carregar requisições
async function carregarRequisicoes() {
    try {
        const termo = document.getElementById('filtroTermoRequisicao').value;
        
        let url = '/api/requisicoes';
        if (termo) {
            url += `?tipo=nome&termo=${encodeURIComponent(termo)}`;
        }
        
        const response = await fetch(url);
        requisicoes = await response.json();
        renderizarRequisicoes();
    } catch (error) {
        console.error('Erro ao carregar requisições:', error);
    }
}

function renderizarRequisicoes() {
    const tbody = document.getElementById('tabelaRequisicoes');
    tbody.innerHTML = '';
    
    requisicoes.forEach(req => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${req.nome}</td>
            <td>${req.email}</td>
            <td>${req.data}</td>
            <td>
                <button class="action-btn expand" onclick="expandirRequisicao(${req.idReq})">EXPANDIR</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

function filtrarRequisicoes() {
    carregarRequisicoes();
}

function limparFiltroRequisicoes() {
    document.getElementById('filtroTermoRequisicao').value = '';
    carregarRequisicoes();
}

// Expandir requisição
function expandirRequisicao(idReq) {
    const req = requisicoes.find(r => r.idReq === idReq);
    if (!req) return;
    
    const detalhes = document.getElementById('detalhesRequisicao');
    detalhes.innerHTML = `
        <div class="detalhes-campo">
            <label>Nome</label>
            <p>${req.nome}</p>
        </div>
        <div class="detalhes-campo">
            <label>E-mail</label>
            <p>${req.email}</p>
        </div>
        <div class="detalhes-campo">
            <label>Data</label>
            <p>${req.data}</p>
        </div>
        <div class="detalhes-campo">
            <label>Justificativa da requisição</label>
            <p>${req.justificativa}</p>
        </div>
        <div class="modal-actions">
            <select id="funcaoRequisicao">
                <option value="">Selecione a função</option>
                ${funcoes.map(f => `<option value="${f.idFuncao}">${f.nome}</option>`).join('')}
            </select>
            <button class="accept" onclick="aceitarRequisicao(${req.idReq})">ACEITAR</button>
            <button class="reject" onclick="recusarRequisicao(${req.idReq})">RECUSAR</button>
        </div>
    `;
    
    document.getElementById('modalExpandirRequisicao').style.display = 'block';
}

function fecharModalRequisicao() {
    document.getElementById('modalExpandirRequisicao').style.display = 'none';
}

// Aceitar requisição
async function aceitarRequisicao(idReq) {
    const idFuncao = parseInt(document.getElementById('funcaoRequisicao').value);
    
    if (!idFuncao) {
        alert('Selecione uma função!');
        return;
    }
    
    try {
        const response = await fetch(`/api/requisicoes/${idReq}/aceitar`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ idFuncao })
        });
        
        if (response.ok) {
            alert('Requisição aceita com sucesso!');
            fecharModalRequisicao();
            carregarRequisicoes();
            carregarUsuarios();
        } else {
            const error = await response.json();
            alert('Erro: ' + error.erro);
        }
    } catch (error) {
        console.error('Erro ao aceitar requisição:', error);
        alert('Erro ao aceitar requisição');
    }
}

// Recusar requisição
async function recusarRequisicao(idReq) {
    if (!confirm('Tem certeza que deseja recusar esta requisição?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/requisicoes/${idReq}/recusar`, {
            method: 'POST'
        });
        
        if (response.ok) {
            alert('Requisição recusada com sucesso!');
            fecharModalRequisicao();
            carregarRequisicoes();
        } else {
            const error = await response.json();
            alert('Erro: ' + error.erro);
        }
    } catch (error) {
        console.error('Erro ao recusar requisição:', error);
        alert('Erro ao recusar requisição');
    }
}

// Fechar modais ao clicar fora
window.onclick = function(event) {
    const modalEditar = document.getElementById('modalEditarUsuario');
    const modalReq = document.getElementById('modalExpandirRequisicao');
    
    if (event.target == modalEditar) {
        fecharModalEditar();
    }
    if (event.target == modalReq) {
        fecharModalRequisicao();
    }
}
