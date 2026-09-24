from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional, List
from models.app import OrgaosPublicosApp
from models.trusted import OrgaosPublicosTrusted
from schemas.schemas import OrgaosPublicosCreate, OrgaosPublicosUpdate

class OrgaosPublicosService:
    def __init__(self, db:Session):
        self.db = db

    #crud
    def create(self, dto: OrgaosPublicosCreate) -> OrgaosPublicosApp:
        opublics = OrgaosPublicosApp (
            nome=dto.nome,
            servico=dto.servico,
            descricao=dto.descricao,
            telefone=dto.telefone,
            email=dto.email,
            site=dto.site,
            endereco=dto.endereco,
            ativo=dto.ativo

        )
        self.db.add(opublics)
        self.db.commit()
        self.db.refresh(opublics)
        return opublics

    def get_by_id(self, opublics_id: int) -> Optional[OrgaosPublicosApp]:
        return self.db.query(OrgaosPublicosApp).filter(OrgaosPublicosApp.id_orgao == opublics_id).first()

    def list_all(self, skip: int = 0, limit = 100) -> List[OrgaosPublicosApp]:
        return self.db.query(OrgaosPublicosApp).offset(skip).limit(limit).all()

    def update(self, opublics_id: int, dto: OrgaosPublicosUpdate) -> Optional[OrgaosPublicosApp]:
        opublics = self.get_by_id(opublics_id)
        if not opublics:
            return None

        update_data = dto.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(opublics, key, value)

        self.db.commit()
        self.db.refresh(opublics)
        return opublics

    #medalhão
    def sync_staging(self) -> None:
        query = text ("""
            INSERT INTO staging.orgaospublicos(id_orgao, nome, servico, descricao, telefone, email, site, endereco, ativo, ingested_at)
            SELECT id_orgao, nome, servico, descricao, telefone, email, site, endereco, ativo, NOW()
            FROM app.orgaospublicos;
        """)
        self.db.execute(query)
        self.db.commit()

    def sync_trusted(self) -> None:
        query = text ("""
            INSERT INTO trusted.orgaospublicos (id_orgao, nome, servico, descricao, telefone, email, site, endereco, ativo, cleaned_at)
            SELECT id_orgao, nome, servico, descricao, telefone, email, site, endereco, ativo, NOW()
            FROM staging.orgaospublicos
            ON CONFLICT (id_orgao) DO UPDATE SET
            nome = EXCLUDED.nome,
            servico = EXCLUDED.servico,
            descricao = EXCLUDED.descricao,
            telefone = EXCLUDED.telefone,
            email = EXCLUDED.email,
            site = EXCLUDED.site,
            endereco = EXCLUDED.endereco,
            ativo = EXCLUDED.ativo,
            cleaned_at = NOW();
        """)
        self.db.execute(query)
        self.db.commit()

    def get_trusted_by_id(self, opublics_id: int) -> Optional[OrgaosPublicosTrusted]:
        return self.db.query(OrgaosPublicosTrusted).filter(OrgaosPublicosTrusted.id_orgao == opublics_id).first()