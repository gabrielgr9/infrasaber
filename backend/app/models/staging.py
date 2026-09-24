from sqlalchemy import Column, Integer, String, DateTime, CheckConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database.database import Base

class UsuariosStaging(Base):
    __tablename__ = "usuarios"
    __table_args__ = {"schema": "staging"}

    id_usuario = Column(Integer, primary_key=True)
    nome = Column(String)
    email = Column(String)
    senha = Column(String)
    tipo = Column(String)
    
    ingested_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
  
class FeedbacksStaging(Base):
    __tablename__ = "feedbacks"
    __table_args__ = (CheckConstraint("nota >= 0 AND nota <=5", name="check_nota_range"),
    {"schema": "staging"})

    id_feedback = Column(Integer, primary_key=True)
    id_usuario = Column(Integer)
    id_problema = Column(Integer)
    nota = Column(Integer)
    comentario = Column(String)
    data_feedback = Column(String)

    ingested_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
  
class CategoriaStaging(Base):
    __tablename__ = "categoria"
    __table_args__ = {"schema": "staging"}
    
    id_categoria = Column(Integer, primary_key=True)
    tipo = Column(String)
    
    ingested_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class ProblemasStaging(Base):
    __tablename__ = "problemas"
    __table_args__ = {"schema": "staging"}

    id_problema = Column(Integer, primary_key=True)
    id_usuario = Column(Integer)
    id_categoria = Column(Integer)
    titulo = Column(String)
    descricao = Column(String)
    endereco = Column(String)
    regiao = Column(String)
    status = Column(String)
    data_registro = Column(String)
    data_atualizacao = Column(String)
    
    ingested_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    

class CursosOficinasStaging(Base):
    __tablename__ = "cursosoficinas"
    __table_args__ = {"schema": "staging"}
    
    id_curso = Column(Integer, primary_key=True)
    nome = Column(String)
    instituicao = Column(String)
    descricao = Column(String)
    modalidade = Column(String)
    data_inicio = Column(String)
    data_fim = Column(String)
    local = Column(String)
    link_externo = Column(String)
    ativo = Column(String)


class PontosInternetStaging(Base):
    __tablename__ = "pontosinternet"
    __table_args__ = {"schema": "staging"}
    
    id_ponto = Column(Integer, primary_key=True)
    nome = Column(String)
    tipo = Column(String)
    endereco = Column(String)
    bairro = Column(String)
    regiao = Column(String)
    horario_funcionamento = Column(String)
    descricao = Column(String)
    link = Column(String)
    ativo = Column(String)
    
    
class IniciativaStaging(Base):
    __tablename__ = "iniciativa"
    __table_args__ = {"schema": "staging"}
    
    id_iniciativa = Column(Integer, primary_key=True)
    nome = Column(String)
    descricao = Column(String)
    responsavel = Column(String)
    endereco = Column(String)
    bairro = Column(String)
    regiao = Column(String)
    data_inicio = Column(String)
    link = Column(String)
    ativo = Column(String)
    
    
class OrgaosPublicosStaging(Base):
    __tablename__ = "orgaospublicos"
    __table_args__ = {"schema": "staging"}
    
    id_orgao = Column(Integer, primary_key=True)
    nome = Column(String)
    servico = Column(String)
    descricao = Column(String)
    telefone = Column(String)
    email = Column(String)
    site = Column(String)
    endereco = Column(String)
    ativo = Column(String)