from typing import List
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Request
from schemas.schemas import UsuariosCreate, UsuariosResponse, UsuariosUpdate, AlterarSenhaDTO
from services.usuarios import UsuariosService
from dependencies import get_usuarios_service, get_current_user
from enums import TipoUsuario
from security import criar_access_token, ACESS_TOKEN_EXPIRE_MINUTES
from models.app import UsuariosApp

router = APIRouter(prefix="/usuarios", tags=["Usuários"])

@router.post("/", response_model=UsuariosResponse, status_code=status.HTTP_201_CREATED)
def criar_usuario(
    dto: UsuariosCreate,
    service: UsuariosService = Depends(get_usuarios_service)
):
    return service.create(dto)

@router.post("/login", status_code=status.HTTP_200_OK)
async def login(
    request: Request,
    service: UsuariosService = Depends(get_usuarios_service)
):
    """
    Rota de login compatível com JSON e Form-Data
    """
    content_type = request.headers.get("content-type", "")
    
    email = None
    senha = None

    if "application/x-www-form-urlencoded" in content_type or "multipart/form-data" in content_type:
        form_data = await request.form()
        email = form_data.get("username") 
        senha = form_data.get("password") 
    else:
        body = await request.json()
        email = body.get("email") or body.get("username")
        senha = body.get("senha") or body.get("password")

    if not email or not senha:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="E-mail e senha são obrigatórios."
        )

    usuario = service.autenticar(email, senha)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="E-mail ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    payload = {
        "sub": usuario.email,
        "id_usuario": usuario.id_usuario,
        "id": usuario.id_usuario,
        "nome": usuario.nome,
        "tipo": usuario.tipo
    }
    
    access_token_expires = timedelta(minutes=ACESS_TOKEN_EXPIRE_MINUTES)
    access_token = criar_access_token(data=payload, expires_delta=access_token_expires)
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

@router.get("/me", response_model=UsuariosResponse)
def ler_conta_atual(usuario_atual: UsuariosApp = Depends(get_current_user)):
    return usuario_atual

@router.get("/tipos", response_model=List[str], status_code=status.HTTP_200_OK)
def listar_tipos_usuario():
    return [tipo.value for tipo in TipoUsuario]

@router.get("/", response_model=List[UsuariosResponse])
def listar_usuarios(
    skip: int = 0,
    limit: int = 100,
    service: UsuariosService = Depends(get_usuarios_service)
):
    return service.list_all(skip=skip, limit=limit)

@router.put("/me/senha", status_code=status.HTTP_200_OK)
def alterar_senha_usuario(
    dto: AlterarSenhaDTO,
    service: UsuariosService = Depends(get_usuarios_service),
    current_user: UsuariosApp = Depends(get_current_user)
):
    """
    Atualiza a senha do usuário logado após validar a senha atual
    """
    sucesso = service.alterar_senha(
        id_usuario=current_user.id_usuario, 
        senha_atual=dto.senha_atual, 
        nova_senha=dto.nova_senha
    )
    
    if not sucesso:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A senha atual está incorreta ou ocorreu um erro ao atualizar."
        )
        
    return {"mensagem": "Senha atualizada com sucesso!"}

@router.put("/{id_usuario}", response_model=UsuariosResponse)
def atualizar_usuario(
    id_usuario: int,
    dto: UsuariosUpdate,
    service: UsuariosService = Depends(get_usuarios_service),
    current_user: UsuariosApp = Depends(get_current_user)
):
    """
    Atualiza o usuário. Admins podem alterar qualquer utilizador utilizadores comuns apenas os próprios dados.
    """
    is_admin = "admin" in str(current_user.tipo).lower()
    
    if not is_admin and current_user.id_usuario != id_usuario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para alterar os dados de outro usuário."
        )

    usuario_atualizado = service.update(id_usuario, dto)
    if not usuario_atualizado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado para atualização!"
        )
    return usuario_atualizado