document.addEventListener("DOMContentLoaded", async () => {
    const token = localStorage.getItem("access_token");
    const tokenType = localStorage.getItem("token_type") || "Bearer";

    if (!token) {
        window.location.href = "/login";
        return;
    }

    // 1. Verifica se o usuário logado é admin para aplicar restrições de tela
    try {
        const resUser = await fetch('/usuarios/me', {
            headers: { 'Authorization': `${tokenType} ${token}` }
        });
        
        if (resUser.ok) {
            const userData = await resUser.json();
            
            if (userData.tipo && userData.tipo.toLowerCase() === 'admin') {
                const formFeedback = document.getElementById("formFeedback");
                if (formFeedback) {
                    Array.from(formFeedback.elements).forEach(element => element.disabled = true);
                }

                const containerMain = document.querySelector(".main-content .container-fluid");
                if (containerMain) {
                    const alerta = document.createElement('div');
                    alerta.className = "alert alert-info mt-2 mb-4";
                    alerta.innerHTML = `<i class="bi bi-info-circle-fill me-2"></i><strong>Modo de Visualização:</strong> Administradores possuem apenas acesso de leitura aos feedbacks.`;
                    containerMain.prepend(alerta);
                }
            }
        }
    } catch (e) {
        console.warn("Aviso ao validar dados do utilizador:", e);
    }

    const formFeedback = document.getElementById("formFeedback");
    if (formFeedback) {
        formFeedback.addEventListener("submit", async (e) => {
            e.preventDefault();
            await enviarFeedback();
        });
    }

    // Carrega o histórico de feedbacks e os pendentes
    carregarHistoricoFeedbacks();
    carregarPendentesFeedback();
});

// Carrega o histórico de feedbacks enviados
async function carregarHistoricoFeedbacks() {
    const tbody = document.getElementById("tabela-com-feedback");
    if (!tbody) return;

    try {
        const token = localStorage.getItem("access_token");
        const tokenType = localStorage.getItem("token_type") || "Bearer";

        const response = await fetch('/feedbacks/', {
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

        if (!response.ok) throw new Error("Erro ao carregar histórico.");

        const feedbacks = await response.json();

        if (!Array.isArray(feedbacks) || feedbacks.length === 0) {
            tbody.innerHTML = `<tr><td colspan="4" class="text-center text-muted py-4">Nenhum feedback registado até ao momento.</td></tr>`;
            return;
        }

        tbody.innerHTML = '';
        feedbacks.forEach(feed => {
            const tr = document.createElement('tr');
            
            // Tratamento e formatação correta da data vinda do backend (data_feedback)
            const dataBruta = feed.data_feedback || feed.data_registro;
            const dataFormatada = dataBruta 
                ? new Date(dataBruta).toLocaleString('pt-BR', { dateStyle: 'short', timeStyle: 'short' }) 
                : '-';

            const nota = feed.nota !== undefined ? feed.nota : '-';
            const comentario = feed.comentario || feed.descricao || '-';
            const descricaoProblema = feed.problema_descricao || `Problema #${feed.id_problema || 'N/A'}`;

            tr.innerHTML = `
                <td class="ps-4"><strong>${descricaoProblema}</strong></td>
                <td><span class="badge bg-primary px-2 py-1">${nota} / 5</span></td>
                <td>${comentario}</td>
                <td><small class="text-muted">${dataFormatada}</small></td>
            `;
            tbody.appendChild(tr);
        });

    } catch (error) {
        console.error("Erro em carregarHistoricoFeedbacks:", error);
        tbody.innerHTML = `<tr><td colspan="4" class="text-center text-danger py-4">Erro ao carregar a tabela de histórico.</td></tr>`;
    }
}

// Carrega os problemas pendentes de feedback para o morador avaliar
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

// Função auxiliar para abrir o modal de feedback preenchendo o ID do problema
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
        // 1. Descobre o ID do usuário logado através da rota /usuarios/me
        const userResponse = await fetch('/usuarios/me', {
            headers: { 'Authorization': `${tokenType} ${token}` }
        });

        if (!userResponse.ok) throw new Error("Não foi possível identificar o usuário logado.");
        const userData = await userResponse.json();
        const idUsuarioLogado = userData.id_usuario;

        const idProblema = document.getElementById("feedbackIdProblema").value;
        const nota = parseInt(document.getElementById("inputNota").value);
        const comentario = document.getElementById("inputComentario").value;

        // 2. Envia o id_usuario junto no corpo da requisição
        const dados = {
            id_usuario: idUsuarioLogado,
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

        let resultado = {};
        try {
            resultado = await response.json();
        } catch (e) {
            console.warn("Resposta não veio em JSON:", e);
        }

        if (response.ok) {
            const modalElement = document.getElementById("modalFeedback");
            const modal = bootstrap.Modal.getInstance(modalElement);
            if (modal) modal.hide();

            const formFeedbackModal = document.getElementById("formFeedback");
            if (formFeedbackModal) formFeedbackModal.reset();

            // Recarrega as listas para remover dos pendentes e adicionar ao histórico
            carregarHistoricoFeedbacks();
            carregarPendentesFeedback();
        } else {
            let mensagemErro = "Erro ao registar o feedback.";
            if (resultado.detail) {
                if (Array.isArray(resultado.detail)) {
                    mensagemErro = resultado.detail.map(err => `${err.loc.join('.')}: ${err.msg}`).join('\n');
                } else {
                    mensagemErro = resultado.detail;
                }
            }
            alert(mensagemErro);
        }
    } catch (error) {
        console.error("Erro ao enviar feedback:", error);
        alert("Erro de conexão ao enviar o feedback.");
    }
}