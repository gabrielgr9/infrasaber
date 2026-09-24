const map = L.map('map').setView([-23.5228, -46.8356], 13);

// Camada de visualização do OpenStreetMap
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Função auxiliar para limpar tipos de dados indesejados no funcionamento (ex: INT, STR)
function limparFuncionamento(texto) {
    if (!texto) return 'Não informado';
    return texto.replace(/^(INT|STR)\s*/i, '').trim();
}

// Função auxiliar para determinar a cor do badge de status (com normalização de acentos)
function obterCorBadgeStatus(status) {
    if (!status) return 'bg-secondary';
    
    const statusNorm = status.normalize("NFD").replace(/[\u0300-\u036f]/g, "").toLowerCase();
    
    if (statusNorm.includes('manutencao')) {
        return 'bg-warning text-dark'; // Amarelo para manutenção
    } else if (statusNorm.includes('inativo')) {
        return 'bg-danger'; // Vermelho para inativo
    }
    return 'bg-success'; // Verde para ativo
}

// Função para carregar e plotar os pontos limpos da camada Trusted (ETL)
async function carregarPontosWifi() {
    try {
        const response = await fetch('/api/wifi/pontos');
        if (!response.ok) {
            throw new Error('Falha ao buscar dados da API');
        }
        
        const pontos = await response.json();
        
        const cardsContainer = document.getElementById('cards-container');
        if (cardsContainer) {
            cardsContainer.innerHTML = ''; // Limpa o contentor antes de preencher
        }

        pontos.forEach(ponto => {
            if (ponto.lat && ponto.lon) {
                // 1. Criação da bolinha azul no lugar do pino padrão
                const marker = L.circleMarker([ponto.lat, ponto.lon], {
                    radius: 8,             // Tamanho da bolinha
                    fillColor: '#0d6efd',  // Azul padrão do Bootstrap
                    color: '#ffffff',      // Borda branca para destacar
                    weight: 2,             // Espessura da borda
                    opacity: 1,
                    fillOpacity: 0.9       // Transparência interna
                }).addTo(map);
                
                // Pop-up dinâmico
                marker.bindPopup(`
                    <div style="font-family: sans-serif;">
                        <b>${ponto.nome || 'Ponto Wi-Fi'}</b><br>
                        <span style="color: #666;">Bairro: ${ponto.bairro || 'Não informado'}</span>
                    </div>
                `);

                // 2. Evento de clique para atualizar o painel lateral com as regras aplicadas
                marker.on('click', () => {
                    const painelLateral = document.getElementById('detalhes-ponto-lateral');
                    if (painelLateral) {
                        const cidadeHtml = ponto.subprefeitura 
                            ? `<p class="mb-2"><strong>Cidade:</strong> ${ponto.subprefeitura}</p>` 
                            : '';

                        const funcionamentoLimpo = limparFuncionamento(ponto.horario_funcionamento);
                        const classeBadge = obterCorBadgeStatus(ponto.status);

                        painelLateral.innerHTML = `
                            <h5 class="fw-bold text-primary mb-3">${ponto.nome || 'Ponto Wi-Fi'}</h5>
                            <p class="mb-2"><strong>Tipo:</strong> ${ponto.tipo || 'Não informado'}</p>
                            <p class="mb-2"><strong>Endereço:</strong> ${ponto.endereco || 'Não informado'}</p>
                            <p class="mb-2"><strong>Bairro:</strong> ${ponto.bairro || 'Não informado'}</p>
                            ${cidadeHtml}
                            <p class="mb-2"><strong>Status:</strong> <span class="badge ${classeBadge}">${ponto.status || 'Ativo'}</span></p>
                            <p class="mb-2"><strong>Funcionamento:</strong> ${funcionamentoLimpo}</p>
                        `;
                    }
                });
            }

            // 3. Renderiza os cartões na secção inferior "Todos os Registros"
            if (cardsContainer) {
                const classeBadgeCard = obterCorBadgeStatus(ponto.status);
                const cardCol = document.createElement('div');
                cardCol.className = 'col';
                cardCol.innerHTML = `
                    <div class="card h-100 shadow-sm border">
                        <div class="card-body">
                            <h5 class="card-title fw-bold fs-6 text-dark">${ponto.nome || 'Ponto Wi-Fi'}</h5>
                            <p class="card-text text-muted small mb-1"><strong>Endereço:</strong> ${ponto.endereco || 'Endereço não especificado'}</p>
                            <p class="card-text text-muted small mb-1"><strong>Bairro:</strong> ${ponto.bairro || 'Não informado'}</p>
                            <span class="badge ${classeBadgeCard}">${ponto.status || 'Ativo'}</span>
                        </div>
                    </div>
                `;
                cardsContainer.appendChild(cardCol);
            }
        });
    } catch (error) {
        console.error('Erro ao renderizar o mapa de Wi-Fi:', error);
    }
}

// Executa a carga ao carregar a página
carregarPontosWifi();