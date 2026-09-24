from typing import List
from fastapi import APIRouter, Depends, status
from schemas.schemas import ProblemasPorCategoriaResponse, PontosWifiPorBairroResponse,ProblemasPorPeriodoResponse, ProblemasPorRegiaoResponse, ProblemasPorStatusResponse
from services.analytics_service import AnalyticsService
from dependencies import get_analytics_service

router = APIRouter(prefix="/analytics", tags=["Dashboard Para Análises"])

@router.get("/por-regiao", response_model=List[ProblemasPorRegiaoResponse], status_code=status.HTTP_200_OK)
def listar_problemas_por_regiao(
    service: AnalyticsService = Depends(get_analytics_service)
):
    return service.get_problemas_por_regiao()

@router.get("/por-categoria", response_model=List[ProblemasPorCategoriaResponse], status_code=status.HTTP_200_OK)
def listar_problemas_por_categoria(
    service: AnalyticsService = Depends(get_analytics_service)
):
    return service.get_problemas_por_categoria()

@router.get("/por-status", response_model=List[ProblemasPorStatusResponse], status_code=status.HTTP_200_OK)
def listar_problemas_por_status(
    service: AnalyticsService = Depends(get_analytics_service)
):
    return service.get_problemas_por_status()

@router.get("/por-periodo", response_model=List[ProblemasPorPeriodoResponse], status_code=status.HTTP_200_OK)
def listar_problemas_por_periodo(
    service: AnalyticsService = Depends(get_analytics_service)
):
    return service.get_problemas_por_periodo()

@router.get("/pontos-wifi-por-bairro", response_model=List[PontosWifiPorBairroResponse], status_code=status.HTTP_200_OK)
def listar_pontos_wifi_por_bairro(
    service: AnalyticsService = Depends(get_analytics_service)
):
    return service.get_pontos_wifi_por_bairro()