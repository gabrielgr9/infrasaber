import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from database.database import init_db
from api import apianalytics, apiwifi, apicategoria, apicursos_oficinas, apifeedbacks, apiiniciativa, apiorgaos_publicos, apipontos_internet, apiproblemas, apiusuarios, paginas

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield
    print("Encerrando aplicação...")

app = FastAPI(
    title="InfraSaber",
    description="Sistema backend para controle de usuarios, orgãos públicos, pontos de internet, cursos, oficinas, problemas e entre outros",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "..", "frontend", "static"))
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

app.include_router(apiusuarios.router)
app.include_router(apicategoria.router)
app.include_router(apicursos_oficinas.router)
app.include_router(apiiniciativa.router)
app.include_router(apiorgaos_publicos.router)
app.include_router(apipontos_internet.router)
app.include_router(apifeedbacks.router)
app.include_router(apiproblemas.router)
app.include_router(apianalytics.router)
app.include_router(apiwifi.router)

app.include_router(paginas.router)

@app.get("/", tags=["Home"])
def read_root():
    return {"message": "Bem-vindos à API do InfraSaber! Acesse /docs para verificar o Swagger"}