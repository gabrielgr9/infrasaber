from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text, func
from database.database import get_db
from models.analytics import PontosWifiPorBairroModel

router = APIRouter(prefix="/api/wifi", tags=["Wi-Fi"])

@router.get("/pontos")
def listar_pontos_wifi(db: Session = Depends(get_db)):
    try:
        query = text("""
            SELECT
                id_ponto_externo AS id,
                nome_local AS nome,
                tipo,
                endereco,
                bairro,
                subprefeitura,
                regiao,
                latitude,
                longitude,
                status,
                horario_funcionamento,
                descricao,
                link
            FROM trusted.pontos_wifi_prefeitura
        """)
        result = db.execute(query).fetchall()

        pontos = [
            {
                "id": row.id,
                "nome": row.nome,
                "tipo": row.tipo,
                "endereco": row.endereco,
                "bairro": row.bairro,
                "subprefeitura": row.subprefeitura,
                "regiao": row.regiao,
                "lat": float(row.latitude) if row.latitude else None,
                "lon": float(row.longitude) if row.longitude else None,
                "status": row.status,
                "horario_funcionamento": row.horario_funcionamento,
                "descricao": row.descricao,
                "link": row.link,
            }
            for row in result
            if row.latitude and row.longitude
        ]
        
        return pontos
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar pontos: {str(e)}")


@router.get("/estatisticas")
def obter_estatisticas_wifi(db: Session = Depends(get_db)):
    try:
        # bus atodas as métricas agregadas diretamente da camada analytics
        totais = db.query(
            func.sum(PontosWifiPorBairroModel.total_pontos).label("total"),
            func.sum(PontosWifiPorBairroModel.total_ativos).label("ativos"),
            func.sum(PontosWifiPorBairroModel.total_manutencao).label("manutencao"),
            func.sum(PontosWifiPorBairroModel.total_inativos).label("inativos")
        ).first()

        return {
            "total": totais.total or 0,
            "ativos": totais.ativos or 0,
            "manutencao": totais.manutencao or 0,
            "inativos": totais.inativos or 0
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar estatísticas: {str(e)}")