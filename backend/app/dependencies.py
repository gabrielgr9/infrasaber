from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from security import SECRET_KEY, ALGORITHM
from models.app import UsuariosApp
from sqlalchemy.orm import Session
from database.database import get_db
from services.usuarios import UsuariosService
from services.categoria import CategoriaService
from services.cursos_oficinas import CursosOficinasService
from services.feedbacks import FeedbacksService
from services.iniciativa import IniciativaService
from services.orgaos_publicos import OrgaosPublicosService
from services.pontos_internet import PontosInternetService
from services.problemas import ProblemasService
from services.analytics_service import AnalyticsService

def get_usuarios_service(db: Session = Depends(get_db)) -> UsuariosService:
  return UsuariosService(db)

def get_categoria_service(db: Session = Depends(get_db)) -> CategoriaService:
  return CategoriaService(db)

def get_feedbacks_service(db: Session = Depends(get_db)) -> FeedbacksService:
  return FeedbacksService(db)

def get_problemas_service(db: Session = Depends(get_db)) -> ProblemasService:
  return ProblemasService(db)

def get_orgaospublicos_service(db: Session = Depends(get_db)) -> OrgaosPublicosService:
  return OrgaosPublicosService(db)

def get_cursosoficinas_service(db: Session = Depends(get_db)) -> CursosOficinasService:
  return CursosOficinasService(db)

def get_iniciativa_service(db: Session = Depends(get_db)) -> IniciativaService:
  return IniciativaService(db)

def get_pontosinternet_service(db: Session = Depends(get_db)) -> PontosInternetService:
  return PontosInternetService(db)

def get_analytics_service(db: Session = Depends(get_db)) -> AnalyticsService:
  return AnalyticsService(db)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/usuarios/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> UsuariosApp:
    """Decodifica o token JWT e retorna o usuário logado."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais de autenticação inválidas ou expiradas",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    usuario = db.query(UsuariosApp).filter(UsuariosApp.email == email).first()
    if usuario is None:
        raise credentials_exception
        
    return usuario

def require_admin(current_user: UsuariosApp = Depends(get_current_user)) -> UsuariosApp:
    """Garante que o usuário logado é do tipo admin (levanta 403 se não for)."""
    tipo_usuario = str(current_user.tipo).lower()
    if "admin" not in tipo_usuario: 
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado: Requer privilégios de administrador"
        )
    return current_user