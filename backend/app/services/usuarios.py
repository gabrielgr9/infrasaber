from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional, List
from models.app import UsuariosApp
from models.trusted import UsuariosTrusted
from schemas.schemas import UsuariosCreate, UsuariosUpdate
from security import gerar_hash_senha, verificar_senha

#crud
class UsuariosService:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, dto: UsuariosCreate) -> UsuariosApp:
        senha_hash = gerar_hash_senha(dto.senha)
        user = UsuariosApp(
            nome=dto.nome,
            email=dto.email,
            senha=senha_hash,
            tipo=dto.tipo
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def get_by_id(self, user_id: int) -> Optional[UsuariosApp]:
        return self.db.query(UsuariosApp).filter(UsuariosApp.id_usuario == user_id).first()
    
    def list_all(self, skip: int=0, limit: int=100) -> List[UsuariosApp]:
        return self.db.query(UsuariosApp).offset(skip).limit(limit).all()
    
    def update(self, user_id: int, dto: UsuariosUpdate) -> Optional[UsuariosApp]:
        user = self.get_by_id(user_id)
        if not user:
            return None

        update_data = dto.model_dump(exclude_unset=True)
        
        if "senha" in update_data and update_data["senha"]:
            update_data["senha"] = gerar_hash_senha(update_data["senha"])
        
        for key, value in update_data.items():
            setattr(user, key, value)
        
        self.db.commit()
        self.db.refresh(user)
        return user
    
    def autenticar(self, email: str, senha_tentativa: str) -> Optional[UsuariosApp]:
        user = self.db.query(UsuariosApp).filter(UsuariosApp.email == email).first()
        if not user:
            return None
        if not verificar_senha(senha_tentativa, user.senha):
            return None
        return user
    
    def alterar_senha(self, id_usuario: int, senha_atual: str, nova_senha: str) -> bool:
        usuario = self.get_by_id(id_usuario)
        if not usuario:
            return False

        #verifica se a senha_atual confere com o hash salvo no banco
        if not verificar_senha(senha_atual, usuario.senha):
            return False

        #gerao hash da nova senha e salvar no banco
        novo_hash = gerar_hash_senha(nova_senha)
        usuario.senha = novo_hash
        self.db.commit()
        self.db.refresh(usuario)
        return True
    
    #medalhão 
    def sync_staging(self) -> None:
        query = text("""
            INSERT INTO staging.usuarios (id_usuario, nome, email, senha, tipo, ingested_at)            
            SELECT id_usuario, nome, email, senha, tipo, NOW()
            FROM app.usuarios;
        """)
        self.db.execute(query)
        self.db.commit()
        
    def sync_trusted(self) -> None:
        query = text("""
            INSERT INTO trusted.usuarios (id_usuario, nome, email, tipo, cleaned_at)            
            SELECT 
                id_usuario, INITCAP(TRIM(nome)), LOWER(email), tipo::TipoUsuario, NOW()
            FROM 
                staging.usuarios
            WHERE
                email IS NOT NULL 
            ON CONFLICT (id_usuario) DO UPDATE SET
                nome = EXCLUDED.nome,
                email = EXCLUDED.email,
                tipo = EXCLUDED.tipo,
                cleaned_at = NOW();
        """)
        self.db.execute(query)
        self.db.commit()
        
    def get_trusted_by_id(self, user_id: int) -> Optional[UsuariosTrusted]:
        return self.db.query(UsuariosTrusted).filter(UsuariosTrusted.id_usuario == user_id).first()