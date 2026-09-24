from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional, List
from models.app import IniciativaApp
from models.trusted import IniciativaTrusted
from schemas.schemas import IniciativaCreate

class IniciativaService:
    def __init__(self, db:Session):
        self.db = db

    #crud
    def create(self, dto: IniciativaCreate) -> IniciativaApp:
        initiative = IniciativaApp (
            nome=dto.nome,
            descricao=dto.descricao,
            responsavel=dto.responsavel,
            endereco=dto.endereco,
            bairro=dto.bairro,
            regiao=dto.regiao,
            data_inicio=dto.data_inicio,
            link=dto.link,
            ativo=dto.ativo
        )
        self.db.add(initiative)
        self.db.commit()
        self.db.refresh(initiative)
        return initiative

    def get_by_id(self, initiative_id: int) -> Optional[IniciativaApp]:
        return self.db.query(IniciativaApp).filter(IniciativaApp.id_iniciativa == initiative_id).first()

    def list_all(self, skip: int = 0, limit = 100) -> List[IniciativaApp]:
        return self.db.query(IniciativaApp).offset(skip).limit(limit).all()

    def update(self, initiative_id: int, dto: IniciativaCreate) -> Optional[IniciativaApp]:
        initiative = self.get_by_id(initiative_id)
        if not initiative:
            return None

        update_data = dto.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(initiative, key, value)

        self.db.commit()
        self.db.refresh(initiative)
        return initiative

    #medalhão
    def sync_staging(self) -> None:
        query = text ("""
            INSERT INTO staging.iniciativa(id_iniciativa, nome, descricao, responsavel, endereco, bairro, regiao, data_inicio, link, ativo, ingested_at)
            SELECT id_iniciativa, nome, descricao, responsavel, endereco, bairro, regiao, data_inicio, link, ativo, NOW()
            FROM app.iniciativa;
        """)
        self.db.execute(query)
        self.db.commit()

    def sync_trusted(self) -> None:
        query = text ("""
            INSERT INTO trusted.iniciativa (id_iniciativa, nome, descricao, responsavel, endereco, bairro, regiao, data_inicio, link, ativo, cleaned_at)
            SELECT id_iniciativa, nome, descricao, responsavel, endereco, bairro, regiao, data_inicio, link, ativo, NOW()
            FROM staging.iniciativa
            ON CONFLICT (id_iniciativa) DO UPDATE SET
            nome = EXCLUDED.nome,
            descricao = EXCLUDED.descricao,
            responsavel = EXCLUDED.responsavel,
            endereco = EXCLUDED.endereco,
            bairro = EXCLUDED.bairro,
            regiao = EXCLUDED.regiao,
            data_inicio = EXCLUDED.data_inicio,
            link = EXCLUDED.link,
            ativo = EXCLUDED.ativo,
            cleaned_at = NOW();
        """)
        self.db.execute(query)
        self.db.commit()

    def get_trusted_by_id(self, initiative_id: int) -> Optional[IniciativaTrusted]:
        return self.db.query(IniciativaTrusted).filter(IniciativaTrusted.id_iniciativa == initiative_id).first()