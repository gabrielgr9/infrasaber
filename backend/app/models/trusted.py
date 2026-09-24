from sqlalchemy import Column, Integer, Numeric, String, Boolean, Date, DateTime, ForeignKey, CheckConstraint, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enums import TipoUsuario, TipoStatus, TipoCategoria
from database.database import Base

class UsuariosTrusted(Base):
    __tablename__ = "usuarios"
    __table_args__ = {"schema": "trusted"}

    id_usuario = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    tipo = Column(Enum(TipoUsuario, native_enum=False), nullable=False)
    
    cleaned_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    feedbacks = relationship("FeedbacksTrusted", back_populates="usuario")
    problemas = relationship("ProblemasTrusted", back_populates="usuario")


class FeedbacksTrusted(Base):
    __tablename__ = "feedbacks"
    __table_args__ = (CheckConstraint("nota >= 0 AND nota <=5", name="check_nota_range"),
    {"schema": "trusted"})

    id_feedback = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("trusted.usuarios.id_usuario"), nullable=False)
    id_problema = Column(Integer, nullable=False)
    nota = Column(Integer, nullable=False)
    comentario = Column(String(300), nullable=False)
    data_feedback = Column(DateTime(timezone=True), server_default=func.now())
    
    cleaned_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    usuario = relationship("UsuariosTrusted", back_populates="feedbacks")


class CategoriaTrusted(Base):
    __tablename__ = "categoria"
    __table_args__ = {"schema": "trusted"}

    id_categoria = Column(Integer, primary_key=True, index=True)
    tipo = Column(Enum(TipoCategoria, native_enum=False), nullable=False)
    
    cleaned_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    problemas = relationship("ProblemasTrusted", back_populates="categoria")


class ProblemasTrusted(Base):
    __tablename__ = "problemas"
    __table_args__ = {"schema": "trusted"}

    id_problema = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("trusted.usuarios.id_usuario"), nullable=False)
    id_categoria = Column(Integer, ForeignKey("trusted.categoria.id_categoria"), nullable=False)
    titulo = Column(String(20), nullable=False)
    descricao = Column(String(300), nullable=False)
    endereco = Column(String(50), nullable=False)
    regiao = Column(String(50), nullable=False)
    status = Column(Enum(TipoStatus, native_enum=False), nullable=False)
    data_registro = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    data_atualizacao = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    
    cleaned_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
    usuario = relationship("UsuariosTrusted", back_populates="problemas")
    categoria = relationship("CategoriaTrusted", back_populates="problemas")


class CursosOficinasTrusted(Base):
    __tablename__ = "cursosoficinas"
    __table_args__ = {"schema": "trusted"}
    
    id_curso = Column(Integer, primary_key=True, index=True)
    nome = Column(String(30), nullable=False)
    instituicao = Column(String(50), nullable=False)
    descricao = Column(String(100), nullable=False)
    modalidade = Column(String(30), nullable=False)
    data_inicio = Column(Date, nullable=False)
    data_fim = Column(Date, nullable=False)
    local = Column(String(100), nullable=False)
    link_externo = Column(String(300), nullable=False)
    ativo = Column(Boolean, server_default='true', nullable=False)

    cleaned_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

class PontosInternetTrusted(Base):
    __tablename__ = "pontosinternet"
    __table_args__ = {"schema": "trusted"}
    
    id_ponto = Column(Integer, primary_key=True, index=True)
    nome = Column(String(30), nullable=False)
    tipo = Column(String(50), nullable=False)
    endereco = Column(String(40), nullable=False)
    bairro = Column(String(40), nullable=False)
    regiao = Column(String(40), nullable=False)
    horario_funcionamento = Column(String(100), nullable=False)
    descricao = Column(String(100), nullable=False)
    link = Column(String(300), nullable=False)
    ativo = Column(Boolean, server_default='true', nullable=False)

    cleaned_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

   
class IniciativaTrusted(Base):
    __tablename__ = "iniciativa"
    __table_args__ = {"schema": "trusted"}
    
    id_iniciativa = Column(Integer, primary_key=True, index=True)
    nome = Column(String(30), nullable=False)
    descricao = Column(String(100), nullable=False)
    responsavel = Column(String(50), nullable=False)
    endereco = Column(String(40), nullable=False)
    bairro = Column(String(40), nullable=False)
    regiao = Column(String(40), nullable=False)
    data_inicio = Column(Date, nullable=False)
    link = Column(String(300), nullable=False)
    ativo = Column(Boolean, server_default='true', nullable=False)

    cleaned_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

 
class OrgaosPublicosTrusted(Base):
    __tablename__ = "orgaospublicos"
    __table_args__ = {"schema": "trusted"}
    
    id_orgao = Column(Integer, primary_key=True, index=True)
    nome = Column(String(30), nullable=False)
    servico = Column(String(50), nullable=False)
    descricao = Column(String(100), nullable=False)
    telefone = Column(String(40), nullable=False)
    email = Column(String(40), nullable=False)
    site = Column(String(300), nullable=False)
    endereco = Column(String(40), nullable=False)
    ativo = Column(Boolean, server_default='true', nullable=False)
    
    cleaned_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    
class PontosWifiPrefeituraTrusted(Base):
    __tablename__ = "pontos_wifi_prefeitura"
    __table_args__ = {"schema": "trusted"}

    id_ponto_externo = Column(String, primary_key=True)
    nome_local = Column(String)
    tipo = Column(String)
    endereco = Column(String)
    bairro = Column(String)
    subprefeitura = Column(String)
    regiao = Column(String)
    latitude = Column(Numeric(precision=10, scale=8))
    longitude = Column(Numeric(precision=11, scale=8))
    status = Column(String)
    horario_funcionamento = Column(String)
    descricao = Column(String)
    link = Column(String, nullable=True)
    cleaned_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)