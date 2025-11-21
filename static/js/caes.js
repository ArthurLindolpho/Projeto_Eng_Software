let caes = [];
let modoEdicao = false;

// Carregar dados iniciais
window.addEventListener('DOMContentLoaded', () => {
    carregarCaes();
});

// Carregar cães
async function carregarCaes() {
    try {
        const tipo = document.getElementById('filtroTipoCao').value;
        const termo = document.getElementById('filtroTermoCao').value;
        
        let url = '/api/caes';
        if (tipo && termo) {
            url += `?tipo=${tipo}&termo=${encodeURIComponent(termo)}`;
        }
        
        const response = await fetch(url);
        caes = await response.json();
        renderizarCaes();
    } catch (error) {
        console.error('Erro ao carregar cães:', error);
    }
}

function renderizarCaes() {
    const tbody = document.getElementById('tabelaCaes');
    tbody.innerHTML = '';
    
    caes.forEach(cao => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${cao.idCao}</td>
            <td>${cao.nome}</td>
            <td>${cao.dataNasc}</td>
            <td>${cao.sexo}</td>
            <td>${cao.status}</td>
            <td>
                <button class="action-btn edit" onclick="abrirModalEditar('${cao.idCao}')">Editar</button>
                <button class="action-btn delete" onclick="removerCao('${cao.idCao}')">Remover</button>
            </td>
        `;
        tbody.appendChild(tr);
    });
}

function filtrarCaes() {
    carregarCaes();
}

function limparFiltroCaes() {
    document.getElementById('filtroTermoCao').value = '';
    carregarCaes();
}

// Adicionar cão
function abrirModalAdicionar() {
    modoEdicao = false;
    document.getElementById('tituloModalCao').textContent = 'Adicionar Novo Cão';
    document.getElementById('formCao').reset();
    document.getElementById('caoIdCao').value = '';
    document.getElementById('modalCao').style.display = 'block';
}

// Editar cão
function abrirModalEditar(idCao) {
    const cao = caes.find(c => c.idCao === idCao);
    if (!cao) return;
    
    modoEdicao = true;
    document.getElementById('tituloModalCao').textContent = 'Editar Cão';
    document.getElementById('caoIdCao').value = cao.idCao;
    document.getElementById('caoNome').value = cao.nome;
    document.getElementById('caoDataNasc').value = cao.dataNasc;
    document.getElementById('caoSexo').value = cao.sexo;
    document.getElementById('caoStatus').value = cao.status;
    
    document.getElementById('modalCao').style.display = 'block';
}

function fecharModalCao() {
    document.getElementById('modalCao').style.display = 'none';
}

// Salvar cão (adicionar ou editar)
async function salvarCao() {
    const nome = document.getElementById('caoNome').value;
    const dataNasc = document.getElementById('caoDataNasc').value;
    const sexo = document.getElementById('caoSexo').value;
    const status = document.getElementById('caoStatus').value;
    
    if (!nome || !dataNasc || !sexo || !status) {
        alert('Todos os campos são obrigatórios!');
        return;
    }
    
    // Validar formato de data
    const dataRegex = /^\d{2}\/\d{2}\/\d{4}$/;
    if (!dataRegex.test(dataNasc)) {
        alert('Data de nascimento inválida! Use o formato DD/MM/AAAA');
        return;
    }
    
    const dados = { nome, dataNasc, sexo, status };
    
    try {
        let response;
        if (modoEdicao) {
            const idCao = document.getElementById('caoIdCao').value;
            response = await fetch(`/api/caes/${idCao}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(dados)
            });
        } else {
            response = await fetch('/api/caes', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(dados)
            });
        }
        
        if (response.ok) {
            alert(modoEdicao ? 'Cão atualizado com sucesso!' : 'Cão adicionado com sucesso!');
            fecharModalCao();
            carregarCaes();
        } else {
            const error = await response.json();
            alert('Erro: ' + error.erro);
        }
    } catch (error) {
        console.error('Erro ao salvar cão:', error);
        alert('Erro ao salvar cão');
    }
}

// Remover cão
async function removerCao(idCao) {
    if (!confirm('Tem certeza que deseja remover este cão?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/caes/${idCao}`, {
            method: 'DELETE'
        });
        
        if (response.ok) {
            alert('Cão removido com sucesso!');
            carregarCaes();
        } else {
            const error = await response.json();
            alert('Erro: ' + error.erro);
        }
    } catch (error) {
        console.error('Erro ao remover cão:', error);
        alert('Erro ao remover cão');
    }
}

// Fechar modal ao clicar fora
window.onclick = function(event) {
    const modal = document.getElementById('modalCao');
    if (event.target == modal) {
        fecharModalCao();
    }
}
