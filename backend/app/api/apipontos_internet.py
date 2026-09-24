from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.schemas import PontosInternetCreate, PontosInternetResponse, PontosInternetUpdate
from services.pontos_internet import PontosInternetService
from dependencies import get_pontosinternet_service

router = APIRouter(prefix="/pontosinternet", tags=["Pontos Internet"])

@router.post("/", response_model=PontosInternetResponse, status_code=status.HTTP_201_CREATED)
def create_pontosinternet(
    dto: PontosInternetCreate,
    service: PontosInternetService = Depends(get_pontosinternet_service)
):
    return service.create(dto)

@router.get("/{id_ponto}", response_model=PontosInternetResponse)
def get_pontointernet_by_id(
    id_ponto: int,
    service: PontosInternetService = Depends(get_pontosinternet_service)
):
    pontosinternet = service.get_by_id(id_ponto)
    if not pontosinternet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ponto de Internet não encontrado!"
        )
    return pontosinternet

@router.get("/", response_model=List[PontosInternetResponse])
def list_pontosinternet(
    skip:int = 0,
    limit: int = 100,
    service: PontosInternetService = Depends(get_pontosinternet_service)
):
    return service.list_all(skip=skip, limit=limit)

@router.put("/{id_ponto}", response_model=PontosInternetResponse)
def update_pontosinternet(
    id_ponto: int,
    dto: PontosInternetUpdate,
    service: PontosInternetService = Depends(get_pontosinternet_service)
):
    updated_pontosinternet = service.update(id_ponto, dto)
    if not updated_pontosinternet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ponto de Internet não encontrado para atualização!"
        )
    return updated_pontosinternet