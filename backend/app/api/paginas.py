import os
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(tags=["Páginas Web"])

API_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(API_DIR, "..", "..", "..", "frontend", "templates")

templates = Jinja2Templates(directory=TEMPLATES_DIR)

@router.get("/mapa", response_class=HTMLResponse)
async def carregar_mapa(request: Request):
    return templates.TemplateResponse(request=request, name="pontos_internet.html", context={"request": request})

@router.get("/dashboard", response_class=HTMLResponse)
async def carregar_dashboard(request: Request):
    return templates.TemplateResponse(request=request, name="dashboard.html", context={"request": request})

@router.get("/problemas", response_class=HTMLResponse)
async def carregar_problemas(request: Request):
    return templates.TemplateResponse(request=request, name="problemas.html", context={"request": request})

@router.get("/iniciativas", response_class=HTMLResponse)
async def carregar_iniciativas(request: Request):
    return templates.TemplateResponse(request=request, name="iniciativas.html", context={"request": request})

@router.get("/cursosoficinas", response_class=HTMLResponse)
async def carregar_iniciativas(request: Request):
    return templates.TemplateResponse(request=request, name="cursos_oficinas.html", context={"request": request})

@router.get("/feedbacks", response_class=HTMLResponse)
async def carregar_iniciativas(request: Request):
    return templates.TemplateResponse(request=request, name="feedbacks.html", context={"request": request})

@router.get("/orgaos", response_class=HTMLResponse)
async def carregar_iniciativas(request: Request):
    return templates.TemplateResponse(request=request, name="orgaos.html", context={"request": request})

@router.get("/conta", response_class=HTMLResponse)
async def carregar_iniciativas(request: Request):
    return templates.TemplateResponse(request=request, name="conta.html", context={"request": request})

@router.get("/login", response_class=HTMLResponse)
async def carregar_iniciativas(request: Request):
    return templates.TemplateResponse(request=request, name="login.html", context={"request": request})