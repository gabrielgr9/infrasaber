from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional, List
from models.app import ProblemasApp
from models.trusted import ProblemasTrusted
from schemas.schemas import ProblemasCreate, ProblemasUpdate
from enums import TipoStatus

class ProblemasService:
    def __init__(self, db:Session):
        self.db = db

        #crud
    def create(self, dto: ProblemasCreate) -> ProblemasApp:
        problems = ProblemasApp(
        id_usuario=dto.id_usuario,
        id_categoria=dto.id_categoria,
        titulo=dto.titulo,
        descricao=dto.descricao,
        endereco=dto.endereco,
        regiao=dto.regiao,
        status=TipoStatus.PENDENTE,
        )
        self.db.add(problems)
        self.db.commit()
        self.db.refresh(problems)
        return problems

    def get_by_id(self, problems_id: int) -> Optional[ProblemasApp]:
        return self.db.query(ProblemasApp).filter(ProblemasApp.id_problema == problems_id).first()

    def list_all(self, skip: int = 0, limit = 100) -> List[ProblemasApp]:
        return self.db.query(ProblemasApp).offset(skip).limit(limit).all()

    def list_by_usuario(self, id_usuario: int, skip: int = 0, limit: int = 100) -> List[ProblemasApp]:
        return (
            self.db.query(ProblemasApp)
            .filter(ProblemasApp.id_usuario == id_usuario)
            .offset(skip)
            .limit(limit)
            .all()
        )
    def update(self, problems_id: int, dto: ProblemasUpdate) -> Optional[ProblemasApp]:
        problems = self.get_by_id(problems_id)
        if not problems:
            return None

        update_data = dto.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(problems, key, value)

        self.db.commit()
        self.db.refresh(problems)
        return problems

        #medalhão
    def sync_staging(self) -> None:
        query = text("""
            INSERT INTO staging.problemas (id_problema, id_usuario, id_categoria, titulo, descricao, endereco, regiao, status, data_registro, data_atualizacao, ingested_at)
            SELECT id_problema, id_usuario, id_categoria, titulo, descricao, endereco, regiao, status, data_registro, data_atualizacao, NOW()
            FROM app.problemas;
        """)
        self.db.execute(query)
        self.db.commit()

    def sync_trusted(self) -> None:
        query = text("""
            INSERT INTO trusted.problemas (id_problema, id_usuario, id_categoria, titulo, descricao, endereco, regiao, status, data_registro, data_atualizacao, cleaned_at)
            SELECT
                    id_problema,
                    id_usuario,
                    id_categoria,
                    titulo,
                    descricao,
                    endereco,
                    regiao,
                    status,
                    data_registro,
                    data_atualizacao,
                    NOW()
            FROM staging.problemas
            ON CONFLICT (id_problema) DO UPDATE SET
            id_usuario = EXCLUDED.id_usuario,
            id_categoria = EXCLUDED.id_categoria,
            titulo = EXCLUDED.titulo,
            descricao = EXCLUDED.descricao,
            endereco = EXCLUDED.endereco,
            regiao = EXCLUDED.regiao,
            status = EXCLUDED.status,
            data_registro = EXCLUDED.data_registro,
            data_atualizacao = EXCLUDED.data_atualizacao,
            cleaned_at = NOW();
        """)
        self.db.execute(query)
        self.db.commit()

    def get_trusted_by_id(self, problems_id:int) -> Optional[ProblemasTrusted]:
        return self.db.query(ProblemasTrusted).filter(ProblemasTrusted.id_problema == problems_id).first()