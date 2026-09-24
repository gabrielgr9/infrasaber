from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional, List
from models.app import CategoriaApp
from models.trusted import CategoriaTrusted
from schemas.schemas import CategoriaCreate

class CategoriaService:
    def __init__(self, db: Session):
        self.db = db
        
    #crud
    def create(self, dto: CategoriaCreate) -> CategoriaApp:
        category = CategoriaApp(
            tipo=dto.tipo
        )
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category
    
    def get_by_id(self, category_id: int) -> Optional[CategoriaApp]:
        return self.db.query(CategoriaApp).filter(CategoriaApp.id_categoria == category_id).first()
    
    def list_all(self, skip: int = 0, limit: int = 100) -> List[CategoriaApp]:
        return self.db.query(CategoriaApp).offset(skip).limit(limit).all()
    
    def update(self, category_id: int, dto: CategoriaCreate) -> Optional[CategoriaApp]:
        category = self.get_by_id(category_id)
        if not category:
            return None
        
        update_data = dto.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(category, key, value)
        
        self.db.commit()
        self.db.refresh(category)
        return category
    
    #medalhão
    def sync_staging(self) -> None:
        query = text("""
            INSERT INTO staging.categoria (id_categoria, tipo, ingested_at)
            SELECT id_categoria, tipo, NOW()
            FROM app.categoria;
        """)
        self.db.execute(query)
        self.db.commit()
    
    def sync_trusted(self) -> None:
        query = text("""
            INSERT INTO trusted.categoria (id_categoria, tipo, cleaned_at)
            SELECT 
                id_categoria, tipo::TipoCategoria, NOW()
            FROM staging.categoria
            ON CONFLICT (id_categoria) DO UPDATE SET
            tipo = EXCLUDED.tipo,
            cleaned_at = NOW();
            """)
        self.db.execute(query)
        self.db.commit()
        
    def get_trusted_by_id(self, category_id: int) -> Optional[CategoriaTrusted]:
        return self.db.query(CategoriaTrusted).filter(CategoriaTrusted.id_categoria == category_id).first()