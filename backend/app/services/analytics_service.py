from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Dict, Any

class AnalyticsService:
    def __init__(self, db: Session):
        self.db = db
    
    def get_problemas_por_categoria(self) -> List[Dict[str, Any]]:
        query = text("""
            SELECT 
                ROW_NUMBER() OVER () as id,
                c.tipo as categoria,
                COUNT(p.id_problema) as total_problemas
            FROM app.problemas p
            JOIN app.categoria c ON p.id_categoria = c.id_categoria
            GROUP BY c.tipo;
        """)
        result = self.db.execute(query).mappings().all()
        return [dict(row) for row in result]
    
    def get_problemas_por_regiao(self) -> List[Dict[str, Any]]:
        query = text("""
            SELECT 
                ROW_NUMBER() OVER () as id,
                COALESCE(NULLIF(TRIM(regiao), ''), 'Não informada') as regiao,
                COUNT(id_problema) as total_problemas
            FROM app.problemas
            GROUP BY COALESCE(NULLIF(TRIM(regiao), ''), 'Não informada')
            ORDER BY regiao DESC;
        """)
        result = self.db.execute(query).mappings().all()
        return [dict(row) for row in result]
    
    def get_problemas_por_status(self) -> List[Dict[str, Any]]:
        query = text("""
            SELECT 
                ROW_NUMBER() OVER () as id,
                status,
                COUNT(id_problema) as quantidade
            FROM app.problemas
            GROUP BY status;
        """)
        result = self.db.execute(query).mappings().all()
        return [dict(row) for row in result]
    
    def get_problemas_por_periodo(self) -> List[Dict[str, Any]]:
        query = text("""
            SELECT 
                ROW_NUMBER() OVER () as id,
                DATE(data_registro) as data_referencia,
                EXTRACT(MONTH FROM data_registro)::INT as mes,
                EXTRACT(YEAR FROM data_registro)::INT as ano,
                SUM(CASE WHEN UPPER(CAST(status AS TEXT)) NOT IN ('CORRIGIDO') THEN 1 ELSE 0 END) as total_abertos,
                SUM(CASE WHEN UPPER(CAST(status AS TEXT)) IN ('CORRIGIDO') THEN 1 ELSE 0 END) as total_resolvidos
            FROM app.problemas
            GROUP BY DATE(data_registro), EXTRACT(MONTH FROM data_registro), EXTRACT(YEAR FROM data_registro)
            ORDER BY data_referencia ASC;
        """)
        result = self.db.execute(query).mappings().all()
        return [dict(row) for row in result]

    def get_pontos_wifi_por_bairro(self) -> List[Dict[str, Any]]:
        query = text("""
            SELECT id, bairro, regiao, total_pontos, total_ativos, total_manutencao, total_inativos
            FROM analytics.pontos_wifi_por_bairro
            ORDER BY total_pontos DESC;
        """)
        result = self.db.execute(query).mappings().all()
        return [dict(row) for row in result]