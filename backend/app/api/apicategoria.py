from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from enums import TipoCategoria 
from schemas.schemas import CategoriaCreate, CategoriaResponse
from services.categoria import CategoriaService
from dependencies import get_categoria_service

router = APIRouter(prefix="/categorias", tags=["Categorias"])

@router.get("/enum", response_model=List[str], status_code=status.HTTP_200_OK)
def listar_enum_categorias():
    return [categoria.value for categoria in TipoCategoria]

@router.post("/", response_model=CategoriaResponse, status_code=status.HTTP_201_CREATED)
def criar_categoria(
    dto: CategoriaCreate,
    service: CategoriaService = Depends(get_categoria_service)
):
    return service.create(dto)

@router.get("/", response_model=List[CategoriaResponse], status_code=status.HTTP_200_OK)
def listar_categorias_cadastradas(
    skip: int = 0,
    limit: int = 100,
    service: CategoriaService = Depends(get_categoria_service)
):
    return service.list_all(skip=skip, limit=limit)