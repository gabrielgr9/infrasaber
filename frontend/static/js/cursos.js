document.addEventListener("DOMContentLoaded", () => {
    carregarCursos();
});

async function carregarCursos() {
    const container = document.getElementById("container-cursos");

    try {
        // Altere a rota no fetch caso no seu backend o prefixo seja /cursos ou /cursosoficinas
        const response = await fetch('/cursos_oficinas');
        if (!response.ok) throw new Error(`Erro HTTP: ${response.status}`);

        let cursos = await response.json();

        // Filtra apenas os cursos com ativo = true
        cursos = cursos.filter(item => item.ativo === true);

        if (cursos.length === 0) {
            container.innerHTML = `
                <div class="col-12 text-center text-muted py-5">
                    <i class="bi bi-journal-x display-4"></i>
                    <p class="mt-2">Nenhum curso ou oficina disponível no momento.</p>
                </div>
            `;
            return;
        }

        container.innerHTML = '';

        cursos.forEach(item => {
            // Formatação das datas
            const dataInicio = item.data_inicio ? new Date(item.data_inicio).toLocaleDateString('pt-BR', {timeZone: 'UTC'}) : 'A definir';
            const dataFim = item.data_fim ? new Date(item.data_fim).toLocaleDateString('pt-BR', {timeZone: 'UTC'}) : 'A definir';

            // Estilização da badge de modalidade (EAD / Presencial / Híbrido)
            let badgeModalidade = 'bg-primary';
            if (item.modalidade && item.modalidade.toUpperCase().includes('EAD')) {
                badgeModalidade = 'bg-info text-dark';
            } else if (item.modalidade && item.modalidade.toUpperCase().includes('PRESENCIAL')) {
                badgeModalidade = 'bg-warning text-dark';
            }

            // Monta o botão de inscrição se houver link
            let linkValido = item.link_externo || item.link;
            let botaoLink = '';
            
            if (linkValido && linkValido.trim() !== '') {
                let urlFinal = linkValido.startsWith('http') ? linkValido : `https://${linkValido}`;
                botaoLink = `
                    <a href="${urlFinal}" target="_blank" class="btn btn-primary btn-sm w-100 mt-3 fw-bold">
                        <i class="bi bi-box-arrow-up-right me-1"></i> Inscrever-se / Mais Informações
                    </a>
                `;
            }

            // Card HTML
            const col = document.createElement('div');
            col.className = 'col-md-6 col-xl-4';

            col.innerHTML = `
                <div class="card card-curso p-4">
                    <div class="card-body">
                        <div class="card-text-content">
                            <div class="d-flex justify-content-between align-items-start mb-2">
                                <div>
                                    <span class="badge ${badgeModalidade} mb-1">${item.modalidade || 'Geral'}</span>
                                    <h5 class="fw-bold text-dark mb-0">${item.nome}</h5>
                                </div>
                                <span class="badge bg-success bg-opacity-10 text-success border border-success border-opacity-25 ms-2">Ativo</span>
                            </div>

                            <p class="text-primary fw-semibold small mb-2">
                                <i class="bi bi-building me-1"></i>${item.instituicao}
                            </p>

                            <p class="text-muted small mb-3">${item.descricao}</p>
                            
                            <hr class="text-muted opacity-25">

                            <ul class="list-unstyled small text-secondary mb-0">
                                <li class="mb-1">
                                    <i class="bi bi-geo-alt-fill text-danger me-2"></i>
                                    <strong>Local:</strong> ${item.local || 'Online'}
                                </li>
                                <li class="mb-1">
                                    <i class="bi bi-calendar-check-fill text-success me-2"></i>
                                    <strong>Período:</strong> ${dataInicio} até ${dataFim}
                                </li>
                            </ul>
                        </div>
                        ${botaoLink}
                    </div>
                </div>
            `;

            container.appendChild(col);
        });

    } catch (error) {
        console.error("Detalhe do erro:", error);
        container.innerHTML = `
            <div class="col-12 text-center text-danger py-5">
                <i class="bi bi-exclamation-triangle display-4"></i>
                <p class="mt-2">Erro ao carregar a lista de cursos e oficinas.</p>
            </div>
        `;
    }
}