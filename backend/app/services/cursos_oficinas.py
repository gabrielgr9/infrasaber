from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional, List
from models.app import CursosOficinasApp
from models.trusted import CursosOficinasTrusted
from schemas.schemas import CursosOficinasCreate

#crud
class CursosOficinasService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, dto:CursosOficinasCreate) -> CursosOficinasApp:
        courses = CursosOficinasApp(
            nome=dto.nome,
            instituicao=dto.instituicao,
            descricao=dto.descricao,
            modalidade=dto.modalidade,
            data_inicio=dto.data_inicio,
            data_fim=dto.data_fim,
            local=dto.local,
            link_externo=dto.link_externo,
            ativo=dto.ativo
        )
        self.db.add(courses)
        self.db.commit()
        self.db.refresh(courses)
        return courses

    def get_by_id(self, course_id: int) -> Optional[CursosOficinasApp]:
        return self.db.query(CursosOficinasApp).filter(CursosOficinasApp.id_curso == course_id).first()

    def list_all (self, skip: int=0, limit: int=100) -> List[CursosOficinasApp]:
        return self.db.query(CursosOficinasApp).offset(skip).limit(limit).all()

    def update(self, course_id: int, dto: CursosOficinasCreate) -> Optional[CursosOficinasApp]:
        courses = self.get_by_id(course_id)
        if not courses:
            return None

        update_data = dto.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(courses, key, value)

        self.db.commit()
        self.db.refresh(courses)
        return courses

    #medalhão
    def sync_staging(self) -> None:
        query = text ("""
            INSERT INTO staging.cursosoficinas (id_curso, nome, instituicao, descricao, modalidade, data_inicio, data_fim, local, link_externo, ativo, ingested_at)
            SELECT id_curso, nome, instituicao, descricao, modalidade, data_inicio, data_fim, local, link_externo, ativo, NOW()
            FROM app.cursosoficinas
        """)
        self.db.execute(query)
        self.db.commit()

    def sync_trusted(self) -> None:
        query = text ("""
            INSERT INTO trusted.cursosoficinas (id_curso, nome, instituicao, descricao, modalidade, data_inicio, data_fim, local, link_externo, ativo, cleaned_at)
            SELECT
                id_curso, nome, instituicao, descricao, modalidade, data_inicio, data_fim, local, link_externo, ativo, NOW()
            FROM
                staging.cursosoficinas
            ON CONFLICT (id_curso) DO UPDATE SET
            nome = EXCLUDED.nome,
            instituicao = EXCLUDED.instituicao,
            descricao = EXCLUDED.descricao,
            modalidade = EXCLUDED.modalidade,
            data_inicio = EXCLUDED.data_inicio,
            data_fim = EXCLUDED.data_fim,
            local = EXCLUDED.local,
            link_externo = EXCLUDED.link_externo,
            ativo = EXCLUDED.ativo,
            cleaned_at = NOW();
        """)
        self.db.execute(query)
        self.db.commit()

    def get_trusted_by_id(self, course_id: int) -> Optional [CursosOficinasTrusted]:
        return self.db.query(CursosOficinasTrusted).filter(CursosOficinasTrusted.id_curso == course_id).first()