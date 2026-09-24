from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.schemas import FeedbacksCreate, FeedbacksResponse
from services.feedbacks import FeedbacksService
from services.usuarios import UsuariosApp
from dependencies import get_feedbacks_service, get_current_user

router = APIRouter(prefix="/feedbacks", tags=["Feedbacks"])

@router.get("/pendentes", response_model=List[dict])
def listar_problemas_pendentes(
    service: FeedbacksService = Depends(get_feedbacks_service),
    current_user: UsuariosApp = Depends(get_current_user)
):
    """Retorna os problemas do usuário logado que ainda não possuem feedback registrado."""
    return service.list_pending_by_user(current_user.id_usuario)

@router.post("/", response_model=FeedbacksResponse, status_code=status.HTTP_201_CREATED)
def criar_feedback(
    dto: FeedbacksCreate,
    service: FeedbacksService = Depends(get_feedbacks_service),
    current_user: UsuariosApp = Depends(get_current_user)
):
    is_admin = "admin" in str(current_user.tipo).lower()
    
    if is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administradores possuem apenas permissão de visualização e não podem enviar feedbacks."
        )

    dto.id_usuario = current_user.id_usuario
    return service.create(dto)

@router.get("/{id_feedback}", response_model=FeedbacksResponse)
def obter_feedback_por_id(
    id_feedback: int,
    service: FeedbacksService = Depends(get_feedbacks_service)
):
    feedback = service.get_by_id(id_feedback)
    if not feedback:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Feedback não encontrado!"
        )
    return feedback

@router.get("/", response_model=List[FeedbacksResponse])
def listar_feedbacks(
    skip: int = 0,
    limit: int = 100,
    service: FeedbacksService = Depends(get_feedbacks_service)
):
    return service.list_all(skip=skip, limit=limit)

@router.put("/{id_feedback}", include_in_schema=False)
@router.patch("/{id_feedback}", include_in_schema=False)
def atualizar_feedback_bloqueado(id_feedback: int):
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="A alteração de feedbacks não é permitida para nenhum tipo de utilizador."
    )

@router.delete("/{id_feedback}", include_in_schema=False)
def deletar_feedback_bloqueado(id_feedback: int):
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="A exclusão de feedbacks não é permitida."
    )