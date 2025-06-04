
document.addEventListener('DOMContentLoaded', function () {
const searchInput = document.getElementById('global-search');
const resultsList = document.getElementById('search-results');

searchInput.addEventListener('input', async function () {
    const q = this.value.trim();
    if (q.length < 2) {
    resultsList.innerHTML = '';
    return;
    }

    try {
    const res = await fetch(`/api/buscar?q=${encodeURIComponent(q)}`);
    const livros = await res.json();
    resultsList.innerHTML = '';

    if (livros.length === 0) {
        resultsList.innerHTML = '<li class="list-group-item text-muted">🔍 Nenhum resultado encontrado</li>';
        return;
    }

    livros.forEach(livro => {
        const li = document.createElement('li');
        li.className = 'list-group-item d-flex justify-content-between align-items-center';
        li.innerHTML = `
        <span><strong>${livro.titulo}</strong> por ${livro.autor}</span>
        <button type="button" class="btn btn-sm btn-outline-primary">➕</button>
        `;
        resultsList.appendChild(li);

        const btn = li.querySelector('button');
        btn.addEventListener('click', () => mostrarOpcoesLivro(livro));
    });
    } catch (err) {
    console.error('Erro ao buscar livros:', err);
    }
});

function mostrarOpcoesLivro(livro) {
    const modalHtml = `
    <div class="modal fade" id="modalOpcoesLivro" tabindex="-1">
        <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
            <h5 class="modal-title">Adicionar "${livro.titulo}"</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
            <button type="button" class="btn btn-outline-success w-100 mb-2" onclick="escolherFila(${livro.id})">➕ Adicionar à Fila</button>
            <button type="button" class="btn btn-outline-info w-100" onclick="escolherLista(${livro.id}, '${livro.titulo}')">➕ Adicionar à Lista</button>
            </div>
        </div>
        </div>
    </div>
    `;

    const container = document.createElement('div');
    container.innerHTML = modalHtml;
    document.body.appendChild(container);
    new bootstrap.Modal(container.querySelector('.modal')).show();
}

window.escolherFila = function (bookId) {
    const anterior = document.getElementById('modalFila');
    if (anterior) anterior.remove();

    const modalHtml = `
    <div class="modal fade" id="modalFila" tabindex="-1">
        <div class="modal-dialog">
        <div class="modal-content">
            <div class="modal-header">
            <h5 class="modal-title">Adicionar à Fila de Leitura</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
            <label for="status-leitura" class="form-label">Status:</label>
            <select id="status-leitura" class="form-select mb-3">
                <option value="reading">📘 Lendo Agora</option>
                <option value="planned" selected>📝 Planejado</option>
                <option value="completed">✅ Concluído</option>
                <option value="skipped">⏩ Ignorado</option>
            </select>

            <label for="posicao-fila" class="form-label">Posição:</label>
            <select id="posicao-fila" class="form-select mb-3">
                <option value="start">📌 Início da fila</option>
                <option value="end" selected>⏩ Fim da fila</option>
            </select>

            <button id="confirmar-fila" class="btn btn-primary w-100">Adicionar</button>
            </div>
        </div>
        </div>
    </div>
    `;
    document.body.insertAdjacentHTML('beforeend', modalHtml);

    const modal = new bootstrap.Modal(document.getElementById('modalFila'));
    modal.show();

    document.getElementById('confirmar-fila').addEventListener('click', async () => {
    const posicao = document.getElementById('posicao-fila').value;
    const status = document.getElementById('status-leitura').value;

    try {
        const res = await fetch(`/add_to_queue/${bookId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: `posicao=${posicao}&status=${status}`
        });

        if (res.ok) {
        mostrarAlertaFada('✅ Livro adicionado à fila com sucesso!');
        setTimeout(() => location.reload(), 1500);
        } else {
        mostrarAlertaFada('❌ Erro ao adicionar livro à fila.');
        }
    } catch (err) {
        console.error(err);
        mostrarAlertaFada('❌ Erro de conexão com o servidor.');
    }
    });
};

window.escolherLista = async function (bookId, titulo) {
    const anterior = document.getElementById('modalLista');
    if (anterior) anterior.remove();

    try {
    const res = await fetch('/api/listas');
    const listas = await res.json();

    let listaOpcoes = '';
    if (listas.length === 0) {
        listaOpcoes = `<p class="text-muted">Nenhuma lista salva.</p>`;
    } else {
        listaOpcoes = listas.map(l => `
        <button class="btn btn-outline-secondary w-100 mb-2 btn-adicionar-lista" data-nome="${l.name}">
            ${l.name}
        </button>
        `).join('');
    }

    const modalHtml = `
        <div class="modal fade" id="modalLista" tabindex="-1">
        <div class="modal-dialog">
            <div class="modal-content">
            <div class="modal-header">
                <h5 class="modal-title">Adicionar "${titulo}" à Lista</h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
            </div>
            <div class="modal-body">
                ${listaOpcoes}
                <a href="/listas/criar" class="btn btn-outline-success w-100">+ Nova Lista</a>
            </div>
            </div>
        </div>
        </div>
    `;

    const container = document.createElement('div');
    container.innerHTML = modalHtml;
    document.body.appendChild(container);
    new bootstrap.Modal(container.querySelector('#modalLista')).show();

    container.querySelectorAll('.btn-adicionar-lista').forEach(botao => {
        botao.addEventListener('click', async () => {
        const listName = botao.dataset.nome;

        try {
            const res = await fetch('/listas/adicionar_por_nome', {
            method: 'POST',
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
            body: `book_id=${bookId}&list_name=${encodeURIComponent(listName)}`
            });

            if (res.ok) {
            mostrarAlertaFada('✅ Livro adicionado à lista com sucesso!');
            setTimeout(() => location.reload(), 1500);
            } else {
            mostrarAlertaFada('❌ Erro ao adicionar livro à lista.');
            }
        } catch (err) {
            console.error(err);
            mostrarAlertaFada('❌ Erro de conexão com o servidor.');
        }
        });
    });

    } catch (err) {
    console.error('Erro ao carregar listas:', err);
    mostrarAlertaFada('Erro ao buscar listas salvas.');
    }
};

document.addEventListener('click', function (e) {
    if (!document.getElementById('search-form').contains(e.target)) {
    resultsList.innerHTML = '';
    }
});
});

function confirmarLimpezaFila(etapa) {
const nomes = {
    'reading': 'Lendo Agora',
    'planned': 'Planejado',
    'completed': 'Concluído',
    'skipped': 'Ignorado'
};
const nomeBonito = nomes[etapa] || etapa;

return confirm(`Tem certeza que deseja esvaziar a etapa "${nomeBonito}" da fila?`) &&
        confirm(`Essa ação removerá todos os livros da etapa "${nomeBonito}". Deseja continuar?`);
}
function confirmarExclusaoLista() {
return confirm('Tem certeza que deseja excluir esta lista?') &&
        confirm('Essa ação é irreversível. Confirmar exclusão da lista?');
}

document.querySelectorAll('.btn-fila').forEach(btn => {
  btn.addEventListener('click', function () {
    const id = this.dataset.bookId;
    escolherFila(id);
  });
});

let alertaFadaModal;

function mostrarAlertaFada(mensagem) {
const alertaEl = document.getElementById('alertaFada');
const msgEl = document.getElementById('mensagem-alerta');
msgEl.textContent = mensagem;

if (!alertaFadaModal) {
    alertaFadaModal = new bootstrap.Modal(alertaEl);
}

alertaFadaModal.show();
}

function confirmarFada(mensagem, callbackConfirmar) {
  document.getElementById('mensagem-confirmacao').textContent = mensagem;

  const botaoConfirmar = document.getElementById('botao-confirmar');
  const modalEl = document.getElementById('modalConfirmacaoFada');
  const modal = new bootstrap.Modal(modalEl);

  botaoConfirmar.replaceWith(botaoConfirmar.cloneNode(true));
  const novoBotao = document.getElementById('botao-confirmar');

  novoBotao.addEventListener('click', () => {
    modal.hide();
    callbackConfirmar();
  });

  modal.show();
}

function confirmarPorDataset(botao) {
    const mensagem = botao.dataset.confirmMsg;
    const formId = botao.dataset.formId;

    confirmarFada(mensagem, function () {
        document.getElementById(formId).submit();
    });
}