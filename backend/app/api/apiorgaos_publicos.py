from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.schemas import OrgaosPublicosCreate, OrgaosPublicosResponse, OrgaosPublicosUpdate
from services.orgaos_publicos import OrgaosPublicosService
from dependencies import get_orgaospublicos_service

router = APIRouter(prefix="/orgaospublicos", tags=["Orgãos Públicos"])

@router.post("/", response_model=OrgaosPublicosResponse, status_code=status.HTTP_201_CREATED)
def create_orgaospublicos(
    dto: OrgaosPublicosCreate,
    service: OrgaosPublicosService = Depends(get_orgaospublicos_service)
):
    return service.create(dto)

@router.get("/{id_orgao}", response_model=OrgaosPublicosResponse)
def get_orgaospublicos(
    id_orgao: int,
    service: OrgaosPublicosService = Depends(get_orgaospublicos_service)
):
    orgaospublicos = service.get_by_id(id_orgao)
    if not orgaospublicos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orgão Público não encontrado!"
        )
    return orgaospublicos

@router.get("/", response_model=List[OrgaosPublicosResponse])
def list_orgaospublicos(
    skip: int = 0,
    limit: int = 100,
    service: OrgaosPublicosService = Depends(get_orgaospublicos_service)
):
    return service.list_all(skip=skip, limit=limit)

@router.put("/{id_orgao}", response_model=OrgaosPublicosResponse)
def update_orgaospublicos(
    id_orgao: int,
    dto: OrgaosPublicosUpdate,
    service: OrgaosPublicosService = Depends(get_orgaospublicos_service)
):
    updated_orgaospublicos = service.update(id_orgao, dto)
    if not updated_orgaospublicos:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Orgão Público não encontrado para atualização!"
        )
    return updated_orgaospublicos

