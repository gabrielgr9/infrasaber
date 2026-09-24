from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional, List
from models.app import PontosInternetApp
from models.trusted import PontosInternetTrusted
from schemas.schemas import PontosInternetCreate, PontosInternetUpdate

class PontosInternetService:
    def __init__(self, db:Session):
        self.db = db

    #crud
    def create(self, dto: PontosInternetCreate) -> PontosInternetApp:
        internet = PontosInternetApp(
            nome=dto.nome,
            tipo=dto.tipo,
            endereco=dto.endereco,
            bairro=dto.bairro,
            regiao=dto.regiao,
            horario_funcionamento=dto.horario_funcionamento,
            descricao=dto.descricao,
            link=dto.link,
            ativo=dto.ativo
        )
        self.db.add(internet)
        self.db.commit()
        self.db.refresh(internet)
        return internet
        
    def get_by_id(self, internet_id: int) -> Optional[PontosInternetApp]:
        return self.db.query(PontosInternetApp).filter(PontosInternetApp.id_ponto == internet_id).first()

    def list_all(self, skip: int = 0, limit =100) -> List[PontosInternetApp]:
        return self.db.query(PontosInternetApp).offset(skip).limit(limit).all()

    def update(self, internet_id: int, dto: PontosInternetUpdate) -> Optional[PontosInternetApp]:
        internet = self.get_by_id(internet_id)
        if not internet:
            return None

        update_data = dto.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(internet, key, value)

        self.db.commit()
        self.db.refresh(internet)
        return internet

    #medalhão
    def sync_staging(self) -> None:
        query = text("""
            INSERT INTO staging.pontosinternet (id_ponto, nome, tipo, endereco, bairro, regiao, horario_funcionamento, descricao, link, ativo, ingested_at)
            SELECT id_ponto, nome, tipo, endereco, bairro, regiao, horario_funcionamento, descricao, link, ativo, NOW()
            FROM app.pontosinternet;
        """)
        self.db.execute(query)
        self.db.commit()

    def sync_trusted(self) -> None:
        query = text ("""
            INSERT INTO trusted.pontosinternet (id_ponto, nome, tipo, endereco, bairro, regiao, horario_funcionamento, descricao, link, ativo, cleaned_at)
            SELECT id_ponto, nome, tipo, endereco, bairro, regiao, horario_funcionamento, descricao, link, ativo, NOW()
            FROM staging.pontosinternet
            ON CONFLICT (id_ponto) DO UPDATE SET
            nome = EXCLUDED.nome,
            tipo = EXCLUDED.tipo,
            endereco = EXCLUDED.endereco,
            bairro = EXCLUDED.bairro,
            regiao = EXCLUDED.regiao,
            horario_funcionamento = EXCLUDED.horario_funcionamento,
            descricao = EXCLUDED.descricao,
            link = EXCLUDED.link,
            ativo = EXCLUDED.ativo,
            cleaned_at = NOW();
        """)
        self.db.execute(query)
        self.db.commit()

    def get_trusted_by_id(self, internet_id:int) -> Optional[PontosInternetTrusted]:
        return self.db.query(PontosInternetTrusted).filter(PontosInternetTrusted.id_ponto == internet_id).first()