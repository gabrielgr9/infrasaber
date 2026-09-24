document.addEventListener("DOMContentLoaded", () => {
    carregarIniciativas();
});

async function carregarIniciativas() {
    const container = document.getElementById("container-iniciativas");

    try {
        // Garantindo a rota correta para o endpoint de iniciativas
        const response = await fetch('/iniciativa');
        if (!response.ok) throw new Error(`Erro HTTP: ${response.status}`);

        let iniciativas = await response.json();

        // Filtra estritamente apenas as ativas
        iniciativas = iniciativas.filter(item => item.ativo === true);

        if (iniciativas.length === 0) {
            container.innerHTML = `
                <div class="col-12 text-center text-muted py-5">
                    <i class="bi bi-info-circle display-4"></i>
                    <p class="mt-2">Nenhuma iniciativa social ativa no momento.</p>
                </div>
            `;
            return;
        }

        container.innerHTML = '';

        iniciativas.forEach(item => {
            const dataFormatada = item.data_inicio ? new Date(item.data_inicio).toLocaleDateString('pt-BR', {timeZone: 'UTC'}) : 'A definir';

            let botaoLink = '';
            if (item.link && item.link.trim() !== '') {
                let urlFinal = item.link.startsWith('http') ? item.link : `https://${item.link}`;
                botaoLink = `
                    <a href="${urlFinal}" target="_blank" class="btn btn-outline-primary btn-sm w-100 mt-3">
                        <i class="bi bi-box-arrow-up-right me-1"></i> Acessar Projeto
                    </a>
                `;
            }

            const col = document.createElement('div');
            col.className = 'col-md-6 col-xl-4';

            col.innerHTML = `
                <div class="card card-iniciativa p-4">
                    <div class="card-body">
                        <div class="card-text-content">
                            <div class="d-flex justify-content-between align-items-start mb-2">
                                <h5 class="fw-bold text-dark mb-0">${item.nome}</h5>
                                <span class="badge bg-success bg-opacity-15 text-white">Ativo</span>
                            </div>
                            <p class="text-muted small mb-3">${item.descricao}</p>
                            
                            <hr class="text-muted opacity-25">

                            <ul class="list-unstyled small text-secondary mb-0">
                                <li class="mb-1"><i class="bi bi-person-fill text-primary me-2"></i><strong>Responsável:</strong> ${item.responsavel}</li>
                                <li class="mb-1"><i class="bi bi-geo-alt-fill text-danger me-2"></i><strong>Endereço:</strong> ${item.endereco} (${item.bairro})</li>
                                <li class="mb-1"><i class="bi bi-map-fill text-info me-2"></i><strong>Região:</strong> ${item.regiao}</li>
                                <li class="mb-1"><i class="bi bi-calendar-event-fill text-success me-2"></i><strong>Início:</strong> ${dataFormatada}</li>
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
                <p class="mt-2">Erro ao carregar as iniciativas sociais. Verifique se há dados cadastrados no banco.</p>
            </div>
        `;
    }
}