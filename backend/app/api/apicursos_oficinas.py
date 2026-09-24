from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from schemas.schemas import CursosOficinasCreate, CursosOficinasResponse, CursosOficinasUpdate
from services.cursos_oficinas import CursosOficinasService
from dependencies import get_cursosoficinas_service

router = APIRouter(prefix="/cursos_oficinas", tags=["CursosOficinas"])

@router.post("/", response_model=CursosOficinasResponse, status_code=status.HTTP_201_CREATED)
def create_cursosoficinas(
    dto: CursosOficinasCreate,
    service: CursosOficinasService = Depends(get_cursosoficinas_service)
):
    return service.create(dto)

@router.get("/{id_curso}", response_model=CursosOficinasResponse)
def get_cursooficinas_by_id(
    id_curso: int,
    service: CursosOficinasService = Depends(get_cursosoficinas_service)
):
    curso = service.get_by_id(id_curso)
    if not curso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso ou Oficina não encontrado!"
        )
    return curso

@router.get("/", response_model=List[CursosOficinasResponse])
def list_cursosoficinas(
    skip: int = 0,
    limit: int = 100,
    service: CursosOficinasService = Depends(get_cursosoficinas_service)
):
    return service.list_all(skip=skip, limit=limit)

@router.put("/{id_curso}", response_model=CursosOficinasResponse)
def update_cursosoficinas(
    id_curso: int,
    dto: CursosOficinasUpdate,
    service: CursosOficinasService = Depends(get_cursosoficinas_service)
):
    updated_cursosoficinas = service.update(id_curso, dto)
    if not updated_cursosoficinas:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Curso ou Oficina não encontrado para atualização!"
        )
    return updated_cursosoficinas