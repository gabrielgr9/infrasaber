document.addEventListener("DOMContentLoaded", () => {
    carregarOrgaosPublicos();
});

async function carregarOrgaosPublicos() {
    const container = document.getElementById("container-orgaos");

    try {
        // Rota ajustada para o padrão correto do backend (/orgaospublicos/)
        const response = await fetch('/orgaospublicos/');
        if (!response.ok) throw new Error(`Erro HTTP: ${response.status}`);

        let orgaos = await response.json();

        // Filtra apenas os órgãos que possuem ativo = true (conforme o model do banco)
        orgaos = orgaos.filter(item => item.ativo === true);

        if (orgaos.length === 0) {
            container.innerHTML = `
                <div class="col-12 text-center text-muted py-5">
                    <i class="bi bi-bank display-4"></i>
                    <p class="mt-2">Nenhum órgão público ativo no momento.</p>
                </div>
            `;
            return;
        }

        container.innerHTML = '';

        orgaos.forEach(item => {
            let botaoSite = '';
            if (item.site && item.site.trim() !== '') {
                let urlFinal = item.site.startsWith('http') ? item.site : `https://${item.site}`;
                botaoSite = `
                    <a href="${urlFinal}" target="_blank" class="btn btn-outline-primary btn-sm w-100 mt-3 fw-semibold">
                        <i class="bi bi-globe me-1"></i> Acessar Site Oficial
                    </a>
                `;
            }

            const col = document.createElement('div');
            col.className = 'col-md-6 col-xl-4';

            col.innerHTML = `
                <div class="card card-orgao p-4">
                    <div class="card-body">
                        <div class="card-text-content">
                            <div class="d-flex justify-content-between align-items-start mb-2">
                                <h5 class="fw-bold text-dark mb-0">${item.nome}</h5>
                                <span class="badge bg-success bg-opacity-15 text-white">Ativo</span>
                            </div>
                            
                            <p class="text-primary fw-semibold small mb-2">
                                <i class="bi bi-tools me-1"></i>${item.servico}
                            </p>

                            <p class="text-muted small mb-3">${item.descricao}</p>
                            
                            <hr class="text-muted opacity-25">

                            <ul class="list-unstyled small text-secondary mb-0">
                                <li class="mb-1">
                                    <i class="bi bi-telephone-fill text-success me-2"></i>
                                    <strong>Telefone:</strong> ${item.telefone}
                                </li>
                                <li class="mb-1">
                                    <i class="bi bi-envelope-fill text-warning me-2"></i>
                                    <strong>E-mail:</strong> ${item.email}
                                </li>
                                <li class="mb-1">
                                    <i class="bi bi-geo-alt-fill text-danger me-2"></i>
                                    <strong>Endereço:</strong> ${item.endereco}
                                </li>
                            </ul>
                        </div>
                        ${botaoSite}
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
                <p class="mt-2">Erro ao carregar a lista de órgãos públicos.</p>
            </div>
        `;
    }
}