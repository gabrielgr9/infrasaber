from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, ForeignKey, CheckConstraint, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enums import TipoUsuario, TipoStatus, TipoCategoria
from database.database import Base


class UsuariosApp(Base):
    __tablename__ = "usuarios"
    __table_args__ = {"schema": "app"}

    id_usuario = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False)
    senha = Column(String(255), nullable=False)
    tipo = Column(Enum(TipoUsuario, native_enum=False), nullable=False)
    
    feedbacks = relationship("FeedbacksApp", back_populates="usuario")
    problemas = relationship("ProblemasApp", back_populates="usuario")

class FeedbacksApp(Base):
    __tablename__ = "feedbacks"
    __table_args__ = (CheckConstraint("nota >= 0 AND nota <=5", name="check_nota_range"),
    {"schema": "app"})

    id_feedback = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("app.usuarios.id_usuario"), nullable=False)
    id_problema = Column(Integer, ForeignKey("app.problemas.id_problema"), nullable=False) # <--- ADICIONE ESTA LINHA
    nota = Column(Integer, nullable=False)
    comentario = Column(String(300), nullable=False)
    data_feedback = Column(DateTime(timezone=True), server_default=func.now())
    
    usuario = relationship("UsuariosApp", back_populates="feedbacks")
    problema = relationship("ProblemasApp") # <--- ADICIONE ESTA RELAÇÃO

class CategoriaApp(Base):
    __tablename__ = "categoria"
    __table_args__ = {"schema": "app"}

    id_categoria = Column(Integer, primary_key=True, index=True)
    tipo = Column(Enum(TipoCategoria, native_enum=False), nullable=False)
    
    problemas = relationship("ProblemasApp", back_populates="categoria")


class ProblemasApp(Base):
    __tablename__ = "problemas"
    __table_args__ = {"schema": "app"}

    id_problema = Column(Integer, primary_key=True, index=True)
    id_usuario = Column(Integer, ForeignKey("app.usuarios.id_usuario"), nullable=False)
    id_categoria = Column(Integer, ForeignKey("app.categoria.id_categoria"), nullable=False)
    titulo = Column(String(100), nullable=False)
    descricao = Column(String(300), nullable=False)
    endereco = Column(String(255), nullable=False)
    regiao = Column(String(255), nullable=False)
    status = Column(Enum(TipoStatus, native_enum=False), nullable=False)
    data_registro = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    data_atualizacao = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    comentario_admin = Column(String, nullable=True)
    atualizado_por = Column(String(100), nullable=True)
    
    usuario = relationship("UsuariosApp", back_populates="problemas")
    categoria = relationship("CategoriaApp", back_populates="problemas")

  
class CursosOficinasApp(Base):
    __tablename__ = "cursosoficinas"
    __table_args__ = {"schema": "app"}
    
    id_curso = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    instituicao = Column(String(255), nullable=False)
    descricao = Column(String(255), nullable=False)
    modalidade = Column(String(50), nullable=False)
    data_inicio = Column(Date, nullable=False)
    data_fim = Column(Date, nullable=False)
    local = Column(String(255), nullable=False)
    link_externo = Column(String(300), nullable=False)
    ativo = Column(Boolean, server_default='true', nullable=False)


class PontosInternetApp(Base):
    __tablename__ = "pontosinternet"
    __table_args__ = {"schema": "app"}
    
    id_ponto = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    tipo = Column(String(255), nullable=False)
    endereco = Column(String(255), nullable=False)
    bairro = Column(String(255), nullable=False)
    regiao = Column(String(255), nullable=False)
    horario_funcionamento = Column(String(100), nullable=False)
    descricao = Column(String(100), nullable=False)
    link = Column(String(300), nullable=False)
    ativo = Column(Boolean, server_default='true', nullable=False)
    
    
class IniciativaApp(Base):
    __tablename__ = "iniciativa"
    __table_args__ = {"schema": "app"}
    
    id_iniciativa = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    descricao = Column(String(255), nullable=False)
    responsavel = Column(String(100), nullable=False)
    endereco = Column(String(255), nullable=False)
    bairro = Column(String(255), nullable=False)
    regiao = Column(String(255), nullable=False)
    data_inicio = Column(Date, nullable=False)
    link = Column(String(300), nullable=False)
    ativo = Column(Boolean, server_default='true', nullable=False)
   
    
class OrgaosPublicosApp(Base):
    __tablename__ = "orgaospublicos"
    __table_args__ = {"schema": "app"}
    
    id_orgao = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    servico = Column(String(255), nullable=False)
    descricao = Column(String(255), nullable=False)
    telefone = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False)
    site = Column(String(255), nullable=False)
    endereco = Column(String(255), nullable=False)
    ativo = Column(Boolean, server_default='true', nullable=False)