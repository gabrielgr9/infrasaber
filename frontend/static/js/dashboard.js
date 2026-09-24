document.addEventListener("DOMContentLoaded", async () => {
    await carregarProblemasPorCategoria();
    await carregarProblemasPorStatus();
    await carregarProblemasPorRegiao();
    await carregarProblemasPorPeriodo();
});

// 1. Gráfico de Pizza: Problemas por Categoria
async function carregarProblemasPorCategoria() {
    try {
        const response = await fetch('/analytics/por-categoria');
        const data = await response.json();

        const labels = data.map(item => item.categoria);
        const valores = data.map(item => item.total_problemas);

        const ctx = document.getElementById('chartCategoria').getContext('2d');
        new Chart(ctx, {
            type: 'pie', // Gráfico de Pizza
            data: {
                labels: labels,
                datasets: [{
                    data: valores,
                    backgroundColor: ['#0f2a4a', '#2a5a91', '#4b88d1', '#7ab0ff', '#b3d3ff', '#1f77b4']
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom' }
                }
            }
        });
    } catch (error) {
        console.error("Erro ao carregar dados de categoria:", error);
    }
}

// 2. Gráfico de Pizza: Problemas por Status
async function carregarProblemasPorStatus() {
    try {
        const response = await fetch('/analytics/por-status');
        const data = await response.json();

        const labels = data.map(item => item.status);
        const valores = data.map(item => item.quantidade);

        const mapaCoresStatus = {
            'pendente': '#ff5507',
            'em_andamento': '#ffc107',
            'corrigido': '#05a01a'
        };

        const backgroundColors = labels.map(status => {
            const statusKey = status ? status.toLowerCase().trim() : '';
            return mapaCoresStatus[statusKey] || '#6c757d';
        });

        const ctx = document.getElementById('chartStatus').getContext('2d');
        new Chart(ctx, {
            type: 'pie', // Gráfico de Pizza
            data: {
                labels: labels,
                datasets: [{
                    data: valores,
                    backgroundColor: backgroundColors
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { position: 'bottom' }
                }
            }
        });
    } catch (error) {
        console.error("Erro ao carregar dados de status:", error);
    }
}

// 3. Região: Nomes + Quantidade em formato de lista estilizada
async function carregarProblemasPorRegiao() {
    try {
        const response = await fetch('/analytics/por-regiao');
        const data = await response.json();

        const listaContainer = document.getElementById('lista-regioes');
        listaContainer.innerHTML = ''; // Limpa o "carregando"

        if (data.length === 0) {
            listaContainer.innerHTML = '<li class="list-group-item text-muted text-center">Nenhuma região registrada.</li>';
            return;
        }

        data.forEach(item => {
            const li = document.createElement('li');
            li.className = 'list-group-item d-flex justify-content-between align-items-center px-0';
            li.innerHTML = `
                <span><i class="bi bi-geo-alt-fill text-primary me-2"></i>${item.regiao}</span>
                <span class="badge bg-primary rounded-pill">${item.total_problemas}</span>
            `;
            listaContainer.appendChild(li);
        });
    } catch (error) {
        console.error("Erro ao carregar dados de região:", error);
    }
}

// 4. Gráfico por Período: Linhas (Abertos vs Resolvidos)
async function carregarProblemasPorPeriodo() {
    try {
        const response = await fetch('/analytics/por-periodo');
        const data = await response.json();

        // Ordena por data caso venha fora de ordem
        data.sort((a, b) => new Date(a.data_referencia) - new Date(b.data_referencia));

        const labels = data.map(item => item.dia || item.data || item.data_referencia);
        const abertos = data.map(item => item.total_abertos !== undefined ? item.total_abertos : (item.abertos !== undefined ? item.abertos : item.total_problemas));
        const resolvidos = data.map(item => item.total_resolvidos !== undefined ? item.total_resolvidos : (item.resolvidos !== undefined ? item.resolvidos : 0));

        const ctx = document.getElementById('chartPeriodo').getContext('2d');
        new Chart(ctx, {
            type: 'line', // Gráfico de linha temporal
            data: {
                labels: labels,
                datasets: [
                    {
                        label: 'Total Abertos',
                        data: abertos,
                        borderColor: '#dc3545',
                        backgroundColor: 'rgba(220, 53, 69, 0.1)',
                        tension: 0.3,
                        fill: true
                    },
                    {
                        label: 'Total Resolvidos',
                        data: resolvidos,
                        borderColor: '#198754',
                        backgroundColor: 'rgba(25, 135, 84, 0.1)',
                        tension: 0.3,
                        fill: true
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    y: { beginAtZero: true }
                },
                plugins: {
                    legend: { position: 'top' }
                }
            }
        });
    } catch (error) {
        console.error("Erro ao carregar dados de período:", error);
    }
}