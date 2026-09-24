from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.schemas import IniciativaCreate, IniciativaResponse, IniciativaUpdate
from services.iniciativa import IniciativaService
from dependencies import get_iniciativa_service

router = APIRouter(prefix="/iniciativa", tags=["Iniciativa"])

@router.post("/", response_model=IniciativaResponse, status_code=status.HTTP_201_CREATED)
def criar_iniciativa(
    dto: IniciativaCreate,
    service: IniciativaService = Depends(get_iniciativa_service)
):
    return service.create(dto)

@router.get("/{id_iniciativa}", response_model=IniciativaResponse)
def get_iniciativa_by_id(
    id_iniciativa: int,
    service: IniciativaService = Depends(get_iniciativa_service)
):
    iniciativa = service.get_by_id(id_iniciativa)
    if not iniciativa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Iniciativa comunitária não encontrada!"
        )
    return iniciativa

@router.get("/", response_model=List[IniciativaResponse])
def list_iniciativa(
    skip: int = 0,
    limit: int = 100,
    service: IniciativaService = Depends(get_iniciativa_service)
):
    return service.list_all(skip=skip, limit=limit)

@router.put("/{id_iniciativa}", response_model=IniciativaResponse)
def update_iniciativa(
    id_iniciativa: int,
    dto: IniciativaUpdate,
    service: IniciativaService = Depends(get_iniciativa_service)
):
    updated_iniciativa = service.update(id_iniciativa, dto)
    if not updated_iniciativa:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Iniciativa comunitária não encontrada para atualizações"
        )
    return updated_iniciativa
