from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional, List
from models.app import FeedbacksApp
from models.trusted import FeedbacksTrusted
from schemas.schemas import FeedbacksCreate, FeedbacksUpdate


class FeedbacksService:
    def __init__(self, db: Session):
        self.db = db

    def create(self, dto: FeedbacksCreate) -> FeedbacksApp:
        feedback = FeedbacksApp(
            id_usuario=dto.id_usuario,
            id_problema=dto.id_problema,
            nota=dto.nota,
            comentario=dto.comentario,
        )
        self.db.add(feedback)
        self.db.commit()
        self.db.refresh(feedback)
        return feedback
    
    def get_by_id(self, feedback_id: int) -> Optional[FeedbacksApp]:
        return self.db.query(FeedbacksApp).filter(FeedbacksApp.id_feedback == feedback_id).first()
    
    def list_all(self, skip: int = 0, limit: int = 100) -> List[FeedbacksApp]:
        return self.db.query(FeedbacksApp).offset(skip).limit(limit).all()
    
    def list_pending_by_user(self, id_usuario: int) -> List[dict]:
        """Busca problemas do usuário que ainda não possuem feedback registrado."""
        query = text("""
            SELECT p.id_problema, p.titulo, p.descricao 
            FROM app.problemas p
            WHERE p.id_usuario = :user_id
              AND p.id_problema NOT IN (
                  SELECT f.id_problema FROM app.feedbacks f WHERE f.id_usuario = :user_id
              )
        """)
        result = self.db.execute(query, {"user_id": id_usuario}).fetchall()
        return [
            {
                "id_problema": row.id_problema,
                "titulo": row.titulo,
                "descricao": row.descricao
            } 
            for row in result
        ]
    
    def update(self, feedback_id: int, dto: FeedbacksUpdate) -> Optional[FeedbacksApp]:
        feedback = self.get_by_id(feedback_id)
        if not feedback:
            return None
        
        update_data = dto.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(feedback, key, value)
        
        self.db.commit()
        self.db.refresh(feedback)
        return feedback
        
    def sync_staging(self) -> None:
        query = text("""
            INSERT INTO staging.feedbacks (id_feedback, id_usuario, id_problema, nota, comentario, data_feedback, ingested_at)
            SELECT id_feedback, id_usuario, id_problema, nota, comentario, data_feedback, NOW()
            FROM app.feedbacks;
        """)
        self.db.execute(query)
        self.db.commit()
        
    def sync_trusted(self) -> None:
        query = text("""
            INSERT INTO trusted.feedbacks (id_feedback, id_usuario, id_problema, nota, comentario, data_feedback, cleaned_at)
            SELECT
                id_feedback,
                id_usuario,
                id_problema,
                nota,
                comentario,
                data_feedback,
                NOW()
            FROM staging.feedbacks
            ON CONFLICT (id_feedback) DO UPDATE SET
                id_problema = EXCLUDED.id_problema,
                nota = EXCLUDED.nota,
                comentario = EXCLUDED.comentario,
                data_feedback = EXCLUDED.data_feedback,
                cleaned_at = NOW(); 
        """)
        self.db.execute(query)
        self.db.commit()
    
    def get_trusted_by_id(self, feedback_id: int) -> Optional[FeedbacksTrusted]:
        return self.db.query(FeedbacksTrusted).filter(FeedbacksTrusted.id_feedback == feedback_id).first()