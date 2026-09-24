from typing import Optional
from datetime import date, datetime
from pydantic import ConfigDict, BaseModel
from enums import TipoUsuario, TipoStatus, TipoCategoria

class LoginDTO(BaseModel):
    email: str
    senha: str
    
class AlterarSenhaDTO(BaseModel):
    senha_atual: str
    nova_senha: str

class UsuariosBase(BaseModel):
    nome: str
    email: str
    tipo: TipoUsuario

class UsuariosCreate(UsuariosBase):
    senha:str

class UsuariosResponse(UsuariosBase):
    id_usuario: int

    model_config = ConfigDict(from_attributes=True)

class UsuariosUpdate(BaseModel):
    nome: Optional[str] = None
    email: Optional[str] = None
    senha: Optional[str] = None
    tipo: Optional[TipoUsuario] = None


class FeedbacksBase(BaseModel):
    nota: int
    comentario: str

class FeedbacksCreate(FeedbacksBase):
    id_usuario: int
    id_problema: int
    nota: int
    comentario: str

class FeedbacksResponse(FeedbacksBase):
    id_feedback: int
    id_problema: int
    id_usuario: int
    data_feedback: datetime
    usuario: UsuariosResponse

    model_config = ConfigDict(from_attributes=True)

class FeedbacksUpdate(BaseModel):
    nota: Optional[int] = None
    comentario: Optional[str] = None
    

class CategoriaBase(BaseModel):
    tipo: TipoCategoria

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaResponse(CategoriaBase):
    id_categoria: int

    model_config = ConfigDict(from_attributes=True)

class CategoriaUpdate(BaseModel):
    tipo: Optional[TipoCategoria] = None
    

class ProblemasBase(BaseModel):
    titulo: str
    descricao: str
    endereco: str
    regiao: str

class ProblemasCreate(ProblemasBase):
    id_usuario: Optional[int] = None
    id_categoria: int
    
class ProblemasResponse(ProblemasBase):
    id_problema: int
    status: TipoStatus
    data_registro: datetime
    data_atualizacao: datetime
    usuario: UsuariosResponse
    categoria: CategoriaResponse
    comentario_admin: Optional[str] = None
    atualizado_por: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class ProblemasUpdate(BaseModel):
    titulo: Optional[str] = None
    descricao: Optional[str] = None
    endereco: Optional[str] = None
    regiao: Optional[str] = None
    id_categoria: Optional[int] = None
    status: Optional[TipoStatus] = None
    comentario_admin: Optional[str] = None
    atualizado_por: Optional[str] = None


class CursosOficinasBase(BaseModel):
    nome: str
    instituicao: str
    descricao: str
    modalidade: str
    data_inicio: date
    data_fim: date
    local: str
    link_externo: str
    ativo: bool = False

class CursosOficinasCreate(CursosOficinasBase):
    pass

class CursosOficinasResponse(CursosOficinasBase):
    id_curso: int

    model_config = ConfigDict(from_attributes=True)

class CursosOficinasUpdate(BaseModel):
    nome: Optional[str] = None
    instituicao: Optional[str] = None
    descricao: Optional[str] = None
    modalidade: Optional[str] = None
    data_inicio: Optional[date] = None
    data_fim: Optional[date] = None
    local: Optional[str] = None
    link_externo: Optional[str] = None
    ativo: Optional[bool] = None


class PontosInternetBase(BaseModel):
    nome: str
    tipo: str
    endereco: str
    bairro: str
    regiao: str
    horario_funcionamento: str
    descricao: str
    link: str
    ativo: bool = False

class PontosInternetCreate(PontosInternetBase):
    pass

class PontosInternetResponse(PontosInternetBase):
    id_ponto: int

    model_config = ConfigDict(from_attributes=True)

class PontosInternetUpdate(BaseModel):
    nome: Optional[str] = None
    tipo: Optional[str] = None
    endereco: Optional[str] = None
    bairro: Optional[str] = None
    regiao: Optional[str] = None
    horario_funcionamento: Optional[str] = None
    descricao: Optional[str] = None
    link: Optional[str] = None
    ativo: Optional[bool] = None
    

class IniciativaBase(BaseModel):
    nome: str
    descricao: str
    responsavel: str
    endereco: str
    bairro: str
    regiao: str
    data_inicio: date
    link: str
    ativo: bool = False

class IniciativaCreate(IniciativaBase):
    pass

class IniciativaResponse(IniciativaBase):
    id_iniciativa: int

    model_config = ConfigDict(from_attributes=True)

class IniciativaUpdate(BaseModel):
    nome: Optional[str] = None
    descricao: Optional[str] = None
    responsavel: Optional[str] = None
    endereco: Optional[str] = None
    bairro: Optional[str] = None
    regiao: Optional[str] = None
    data_inicio: Optional[date] = None
    link: Optional[str] = None
    ativo: Optional[bool] = None


class OrgaosPublicosBase(BaseModel):
    nome: str
    servico: str
    descricao: str
    telefone: str
    email: str
    site: str
    endereco: str
    ativo: bool = False

class OrgaosPublicosCreate(OrgaosPublicosBase):
    pass

class OrgaosPublicosResponse(OrgaosPublicosBase):
    id_orgao: int

    model_config = ConfigDict(from_attributes=True)

class OrgaosPublicosUpdate(BaseModel):
    nome: Optional[str] = None
    servico: Optional[str] = None
    descricao: Optional[str] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    site: Optional[str] = None
    endereco: Optional[str] = None
    ativo: Optional[bool] = None
    

class ProblemasPorCategoriaResponse(BaseModel):
    id: int
    categoria: str
    total_problemas: int
    
    model_config = ConfigDict(from_attributes=True)
    
class ProblemasPorRegiaoResponse(BaseModel):
    id: int
    regiao: str
    total_problemas: int
    
    model_config = ConfigDict(from_attributes=True)
    
class ProblemasPorStatusResponse(BaseModel):
    id: int
    status: str
    quantidade: int
    
    model_config = ConfigDict(from_attributes=True)
    
class ProblemasPorPeriodoResponse(BaseModel):
    id: int
    data_referencia: date
    ano: int
    mes: int
    total_abertos: int
    total_resolvidos: int
    
    model_config = ConfigDict(from_attributes=True)

class PontosWifiPorBairroResponse(BaseModel):
    id: int
    bairro: str
    regiao: str
    total_pontos: int
    total_ativos: int

    model_config = ConfigDict(from_attributes=True)