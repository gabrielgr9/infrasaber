from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.schemas import ProblemasCreate, ProblemasResponse, ProblemasUpdate
from services.problemas import ProblemasService
from dependencies import get_problemas_service, get_current_user
from models.app import UsuariosApp

router = APIRouter(prefix="/problemas", tags=["Problemas"])

@router.post("/", response_model=ProblemasResponse, status_code=status.HTTP_201_CREATED)
def criar_problema(
    dto: ProblemasCreate,
    service: ProblemasService = Depends(get_problemas_service),
    current_user: UsuariosApp = Depends(get_current_user)
):
    dto.id_usuario = current_user.id_usuario
    return service.create(dto)

@router.get("/{id_problema}", response_model=ProblemasResponse)
def obter_problema_por_id(
    id_problema: int,
    service: ProblemasService = Depends(get_problemas_service),
    current_user: UsuariosApp = Depends(get_current_user)
):
    problema = service.get_by_id(id_problema)
    if not problema:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Problema não encontrado!"
        )
    
    # se não for como admin, impede que veja o problema de outro usuário
    is_admin = "admin" in str(current_user.tipo).lower()
    if not is_admin and problema.id_usuario != current_user.id_usuario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Você não tem permissão para acessar este problema."
        )
        
    return problema

@router.get("/", response_model=List[ProblemasResponse])
def listar_problemas(
    skip: int = 0,
    limit: int = 100,
    service: ProblemasService = Depends(get_problemas_service),
    current_user: UsuariosApp = Depends(get_current_user)
):
    is_admin = "admin" in str(current_user.tipo).lower()
    
    if is_admin:
        return service.list_all(skip=skip, limit=limit)
    else:
        return service.list_by_usuario(id_usuario=current_user.id_usuario, skip=skip, limit=limit)

@router.put("/{id_problema}", response_model=ProblemasResponse)
def atualizar_problema(
    id_problema: int,
    dto: ProblemasUpdate,
    service: ProblemasService = Depends(get_problemas_service),
    current_user: UsuariosApp = Depends(get_current_user)
):
    is_admin = "admin" in str(current_user.tipo).lower()

    problema = service.get_by_id(id_problema)
    if not problema:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Problema não encontrado!")

    if is_admin:
        dto.atualizado_por = current_user.nome
        return service.update(id_problema, dto)

    if problema.id_usuario != current_user.id_usuario:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Você não tem permissão para alterar o problema de outro usuário.")

    return service.update(id_problema, dto)