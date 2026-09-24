let problemasCache = [];
let isAdminGlobal = false;

function carregarProblemas() {
    carregarChamadosTabela(isAdminGlobal);
}

document.addEventListener("DOMContentLoaded", async () => {
    const token = localStorage.getItem("access_token");
    const tokenType = localStorage.getItem("token_type") || "Bearer";

    if (!token) {
        window.location.href = "/login";
        return;
    }

    let isAdmin = false;

    // 1. Verifica se o usuário logado é admin
    try {
        const resUser = await fetch('/usuarios/me', {
            headers: { 'Authorization': `${tokenType} ${token}` }
        });

        if (resUser.ok) {
            const userData = await resUser.json();

            if (userData.tipo && userData.tipo.toLowerCase() === 'admin') {
                isAdmin = true;
                isAdminGlobal = true;

                const formFeedback = document.getElementById("formFeedback");
                if (formFeedback) {
                    Array.from(formFeedback.elements).forEach(element => element.disabled = true);
                }

                const formProblemaEl = document.getElementById("form-problema");
                if (formProblemaEl) {
                    Array.from(formProblemaEl.elements).forEach(element => element.disabled = true);
                }

                const containerMain = document.querySelector(".main-content .container-fluid");
                if (containerMain) {
                    const alerta = document.createElement('div');
                    alerta.className = "alert alert-info mt-2 mb-4";
                    alerta.innerHTML = `<i class="bi bi-shield-lock-fill me-2"></i><strong>Painel Administrativo:</strong> Busque pelo ID do problema abaixo ou selecione na tabela para gerenciar o status e atualizar o acompanhamento visível aos moradores.`;
                    containerMain.prepend(alerta);

                    const painelAdminBusca = document.createElement('div');
                    painelAdminBusca.className = "card shadow-sm p-4 mb-4 bg-light";
                    painelAdminBusca.innerHTML = `
                        <h5 class="fw-bold mb-3"><i class="bi bi-search me-2"></i>Gerenciar Problema por ID</h5>
                        <div class="row g-3 align-items-end">
                            <div class="col-md-3">
                                <label for="adminBuscaId" class="form-label">ID do Problema</label>
                                <input type="number" id="adminBuscaId" class="form-control" placeholder="Ex: 1">
                            </div>
                            <div class="col-md-3">
                                <button class="btn btn-primary w-100" onclick="buscarProblemaPorIdAdmin()">
                                    <i class="bi bi-arrow-right-circle me-1"></i> Carregar Dados
                                </button>
                            </div>
                        </div>

                        <div id="formEdicaoAdminContainer" class="mt-4" style="display: none;">
                            <hr>
                            <h6 class="fw-bold text-secondary mb-3">Detalhes do Problema Carregado:</h6>
                            <p class="mb-1"><strong>Título/Descrição Original:</strong> <span id="adminInfoDescricao">-</span></p>
                            <p class="mb-3"><strong>Morador ID:</strong> <span id="adminInfoUsuario">-</span></p>

                            <div class="mb-3">
                                <label for="adminSelectStatus" class="form-label">Alterar Status</label>
                                <select id="adminSelectStatus" class="form-select">
                                    <option value="pendente">Pendente</option>
                                    <option value="em_andamento">Em Andamento</option>
                                    <option value="corrigido">Corrigido</option>
                                </select>
                            </div>

                            <div class="mb-3">
                                <label for="adminInputComentario" class="form-label">Texto Informativo para os Moradores (O que está sendo feito)</label>
                                <textarea id="adminInputComentario" class="form-control" rows="3" placeholder="Descreva o andamento ou a solução aplicada..."></textarea>
                            </div>

                            <button class="btn btn-success" onclick="salvarAtualizacaoProblemaAdmin()">
                                <i class="bi bi-check-lg me-1"></i> Salvar Alterações
                            </button>
                        </div>
                    `;
                    containerMain.insertBefore(painelAdminBusca, containerMain.children[1]);
                }
            }
        }
    } catch (e) {
        console.warn("Aviso ao validar dados do utilizador:", e);
    }

    await carregarCategorias();
    ativarFormularioProblema(isAdmin);
    carregarChamadosTabela(isAdmin);

    if (!isAdmin) {
        carregarPendentesFeedback();
    }
});

let idProblemaEmEdicao = null;

async function carregarCategorias() {
    const select = document.getElementById("id_categoria");
    if (!select) return;
    try {
        const response = await fetch('/categorias/');
        if (!response.ok) throw new Error("Erro ao buscar categorias");
        const categorias = await response.json();

        select.innerHTML = '<option value="" selected disabled>Selecione uma categoria</option>';
        categorias.forEach(cat => {
            const opt = document.createElement('option');
            opt.value = cat.id_categoria;
            opt.textContent = cat.tipo;
            select.appendChild(opt);
        });
    } catch (error) {
        console.error("Erro ao carregar categorias:", error);
        select.innerHTML = '<option value="" selected disabled>Erro ao carregar categorias</option>';
    }
}

function ativarFormularioProblema(isAdmin) {
    const formProblema = document.getElementById("form-problema");
    if (!formProblema || isAdmin) return;

    formProblema.addEventListener("submit", async (e) => {
        e.preventDefault();

        const token = localStorage.getItem("access_token");
        const tokenType = localStorage.getItem("token_type") || "Bearer";

        const dados = {
            titulo: document.getElementById("titulo").value,
            id_categoria: parseInt(document.getElementById("id_categoria").value),
            endereco: document.getElementById("endereco").value,
            regiao: document.getElementById("regiao").value,
            descricao: document.getElementById("descricao").value
        };

        try {
            const response = await fetch('/problemas/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `${tokenType} ${token}`
                },
                body: JSON.stringify(dados)
            });

            if (response.ok) {
                alert("Problema relatado com sucesso!");
                formProblema.reset();
                carregarChamadosTabela(isAdmin);
            } else {
                const err = await response.json();
                let mensagemErro = 'Erro ao relatar problema.';
                if (Array.isArray(err.detail)) {
                    mensagemErro = err.detail.map(e => `${e.loc.join('.')}: ${e.msg}`).join('\n');
                } else if (err.detail) {
                    mensagemErro = err.detail;
                }
                alert(mensagemErro);
            }
        } catch (error) {
            console.error("Erro ao enviar problema:", error);
            alert("Erro de conexão ao enviar o relato.");
        }
    });
}

async function carregarChamadosTabela(isAdmin) {
    const tbody = document.getElementById("tabela-problemas");
    if (!tbody) return;

    try {
        const token = localStorage.getItem("access_token");
        const tokenType = localStorage.getItem("token_type") || "Bearer";

        const response = await fetch('/problemas/', {
            method: 'GET',
            headers: {
                'Authorization': `${tokenType} ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.status === 401) {
            localStorage.removeItem("access_token");
            localStorage.removeItem("token_type");
            window.location.href = "/login";
            return;
        }

        if (!response.ok) throw new Error("Erro ao carregar chamados.");

        const problemas = await response.json();
        problemasCache = problemas; // guarda pra abrir o modal sem precisar buscar de novo

        if (!Array.isArray(problemas) || problemas.length === 0) {
            tbody.innerHTML = `<tr><td colspan="7" class="text-center text-muted py-4">Nenhum chamado registrado até o momento.</td></tr>`;
            return;
        }

        tbody.innerHTML = '';
        problemas.forEach(prob => {
            const tr = document.createElement('tr');
            const idProb = prob.id_problema || prob.id;
            const titulo = prob.titulo || `Problema #${idProb}`;
            const statusAtual = prob.status || 'pendente';
            const categoriaTxt = prob.categoria?.tipo ?? '-';
            const registro = prob.data_registro ? new Date(prob.data_registro).toLocaleDateString() : '-';

            let badgeStatus = 'bg-secondary';
            if (statusAtual === 'pendente') badgeStatus = 'bg-danger';
            if (statusAtual === 'em_andamento') badgeStatus = 'bg-warning text-dark';
            if (statusAtual === 'corrigido') badgeStatus = 'bg-success';

            // Botão "Detalhes" (com o texto de correção) aparece pros dois perfis
            const btnDetalhes = `<button class="btn btn-sm btn-outline-secondary" onclick="abrirDetalhesProblema(${idProb})" title="Ver texto de correção"><i class="bi bi-info-circle"></i></button>`;

            const colunaFinal = isAdmin
                ? `<td class="text-end pe-4 d-flex gap-2 justify-content-end">
                       <button class="btn btn-sm btn-outline-primary" onclick="preencherBuscaAdmin(${idProb})"><i class="bi bi-pencil-square"></i> Selecionar</button>
                       ${btnDetalhes}
                   </td>`
                : `<td class="text-end pe-4">${btnDetalhes}</td>`;

            tr.innerHTML = `
                <td class="ps-4">#${idProb}</td>
                <td>${titulo}</td>
                <td>${categoriaTxt}</td>
                <td>${prob.endereco ?? '-'} / ${prob.regiao ?? '-'}</td>
                <td><span class="badge ${badgeStatus} px-2 py-1">${statusAtual.toUpperCase()}</span></td>
                <td><small>${registro}</small></td>
                ${colunaFinal}
            `;
            tbody.appendChild(tr);
        });

    } catch (error) {
        console.error("Erro ao carregar tabela de chamados:", error);
        tbody.innerHTML = `<tr><td colspan="7" class="text-center text-danger py-4">Erro ao carregar os chamados.</td></tr>`;
    }
}

// Abre o modal com o texto de correção, pra moradores e admin
function abrirDetalhesProblema(idProblema) {
    const prob = problemasCache.find(p => (p.id_problema || p.id) === idProblema);
    if (!prob) return;

    const statusAtual = prob.status || 'pendente';
    let badgeStatus = 'bg-secondary';
    if (statusAtual === 'pendente') badgeStatus = 'bg-danger';
    if (statusAtual === 'em_andamento') badgeStatus = 'bg-warning text-dark';
    if (statusAtual === 'corrigido') badgeStatus = 'bg-success';

    document.getElementById("detalheTitulo").textContent = prob.titulo || `Problema #${idProblema}`;
    document.getElementById("detalheStatus").textContent = statusAtual.toUpperCase();
    document.getElementById("detalheStatus").className = `badge ${badgeStatus}`;
    document.getElementById("detalheCategoria").textContent = prob.categoria?.tipo ?? '-';
    document.getElementById("detalheEndereco").textContent = `${prob.endereco ?? '-'} / ${prob.regiao ?? '-'}`;
    document.getElementById("detalheDescricao").textContent = prob.descricao || 'Sem descrição informada.';
    document.getElementById("detalheComentarioAdmin").innerHTML = prob.comentario_admin
        ? `${prob.comentario_admin}<br><small class="text-muted">Atualizado por: ${prob.atualizado_por || 'Administração'} em ${prob.data_atualizacao ? new Date(prob.data_atualizacao).toLocaleString('pt-BR') : '-'}</small>`
        : 'Aguardando análise da administração...';

    const modalElement = document.getElementById("modalDetalhesProblema");
    if (modalElement) {
        const modal = new bootstrap.Modal(modalElement);
        modal.show();
    }
}

async function buscarProblemaPorIdAdmin() {
    const idInput = document.getElementById("adminBuscaId").value;
    if (!idInput) {
        alert("Por favor, insira um ID de problema válido.");
        return;
    }

    const token = localStorage.getItem("access_token");
    const tokenType = localStorage.getItem("token_type") || "Bearer";

    try {
        const response = await fetch(`/problemas/${idInput}`, {
            headers: { 'Authorization': `${tokenType} ${token}` }
        });

        if (!response.ok) {
            alert("Problema não encontrado.");
            document.getElementById("formEdicaoAdminContainer").style.display = "none";
            return;
        }

        const prob = await response.json();
        idProblemaEmEdicao = prob.id_problema || prob.id;

        document.getElementById("adminInfoDescricao").innerText = prob.descricao || prob.titulo || 'Sem descrição';
        document.getElementById("adminInfoUsuario").innerText = prob.id_usuario || 'N/A';
        document.getElementById("adminSelectStatus").value = prob.status || 'pendente';
        document.getElementById("adminInputComentario").value = prob.comentario_admin || '';

        document.getElementById("formEdicaoAdminContainer").style.display = "block";

    } catch (error) {
        console.error("Erro ao buscar problema:", error);
        alert("Erro de conexão ao buscar o problema.");
    }
}

async function salvarAtualizacaoProblemaAdmin() {
    if (!idProblemaEmEdicao) return;

    const novoStatus = document.getElementById("adminSelectStatus").value;
    const comentarioAdmin = document.getElementById("adminInputComentario").value;

    const token = localStorage.getItem("access_token");
    const tokenType = localStorage.getItem("token_type") || "Bearer";

    try {
        const response = await fetch(`/problemas/${idProblemaEmEdicao}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `${tokenType} ${token}`
            },
            body: JSON.stringify({
                status: novoStatus,
                comentario_admin: comentarioAdmin
            })
        });

        if (response.ok) {
            alert("Problema atualizado com sucesso! Os moradores já conseguem visualizar o novo status e o texto informativo.");
            document.getElementById("formEdicaoAdminContainer").style.display = "none";
            document.getElementById("adminBuscaId").value = '';
            carregarChamadosTabela(true);
        } else {
            const err = await response.json();
            alert("Erro ao atualizar: " + (err.detail || 'Erro desconhecido'));
        }
    } catch (error) {
        console.error("Erro na requisição:", error);
        alert("Erro de conexão ao salvar as alterações.");
    }
}

function preencherBuscaAdmin(idProblema) {
    document.getElementById("adminBuscaId").value = idProblema;
    buscarProblemaPorIdAdmin();
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

async function carregarPendentesFeedback() {
    const container = document.getElementById("container-sem-feedback");
    if (!container) return;

    try {
        const token = localStorage.getItem("access_token");
        const tokenType = localStorage.getItem("token_type") || "Bearer";

        const response = await fetch('/feedbacks/pendentes', {
            method: 'GET',
            headers: {
                'Authorization': `${tokenType} ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (!response.ok) {
            container.innerHTML = `<div class="col-12 text-center text-muted py-3">Nenhum problema pendente de avaliação no momento.</div>`;
            return;
        }

        const pendentes = await response.json();

        if (!Array.isArray(pendentes) || pendentes.length === 0) {
            container.innerHTML = `<div class="col-12 text-center text-muted py-3">Não há problemas aguardando sua avaliação.</div>`;
            return;
        }

        container.innerHTML = '';
        pendentes.forEach(prob => {
            const col = document.createElement('div');
            col.className = "col-md-4 mb-3";
            const idProb = prob.id_problema || prob.id;
            const tituloProb = prob.titulo || `Problema #${idProb}`;
            const descProb = prob.descricao || 'Sem descrição informada.';

            col.innerHTML = `
                <div class="card card-pendente p-3 h-100 d-flex flex-column justify-content-between shadow-sm">
                    <div>
                        <h5 class="fw-bold text-dark">#${idProb} - ${tituloProb}</h5>
                        <p class="text-muted small mb-3">${descProb}</p>
                    </div>
                    <button class="btn btn-outline-primary btn-sm mt-auto" onclick="abrirModalFeedback(${idProb})">
                        <i class="bi bi-star me-1"></i> Avaliar Problema
                    </button>
                </div>
            `;
            container.appendChild(col);
        });

    } catch (error) {
        console.error("Erro ao carregar pendentes:", error);
        container.innerHTML = `<div class="col-12 text-center text-muted py-3">Erro ao carregar problemas pendentes.</div>`;
    }
}

function abrirModalFeedback(idProblema) {
    const inputId = document.getElementById("feedbackIdProblema");
    if (inputId) {
        inputId.value = idProblema;
    }
    const modalElement = document.getElementById("modalFeedback");
    if (modalElement) {
        const modal = new bootstrap.Modal(modalElement);
        modal.show();
    }
}

async function enviarFeedback() {
    const token = localStorage.getItem("access_token");
    const tokenType = localStorage.getItem("token_type") || "Bearer";

    if (!token) {
        alert("Você precisa estar logado.");
        window.location.href = "/login";
        return;
    }

    try {
        const userResponse = await fetch('/usuarios/me', {
            headers: { 'Authorization': `${tokenType} ${token}` }
        });

        if (!userResponse.ok) throw new Error("Não foi possível identificar o usuário logado.");
        const userData = await userResponse.json();

        const idProblema = document.getElementById("feedbackIdProblema").value;
        const nota = parseInt(document.getElementById("inputNota").value);
        const comentario = document.getElementById("inputComentario").value;

        const dados = {
            id_usuario: userData.id_usuario,
            id_problema: parseInt(idProblema),
            nota: nota,
            comentario: comentario
        };

        const response = await fetch('/feedbacks/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `${tokenType} ${token}`
            },
            body: JSON.stringify(dados)
        });

        if (response.ok) {
            const modalElement = document.getElementById("modalFeedback");
            const modal = bootstrap.Modal.getInstance(modalElement);
            if (modal) modal.hide();

            document.getElementById("formFeedback").reset();
            carregarChamadosTabela(false);
            carregarPendentesFeedback();
        } else {
            alert("Erro ao registar o feedback.");
        }
    } catch (error) {
        console.error("Erro ao enviar feedback:", error);
    }
}