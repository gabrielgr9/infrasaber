from datetime import date
from sqlalchemy import Integer, String, Date
from sqlalchemy.orm import Mapped, mapped_column
from database.database import Base

class ProblemasPorCategoriaModel(Base):
    __tablename__ = "problemas_por_categoria"
    __table_args__ = {"schema": "analytics"}
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    categoria: Mapped[str] = mapped_column(String(50), index=True)
    total_problemas: Mapped[int] = mapped_column(Integer)
    
class ProblemasPorRegiaoModel(Base):
    __tablename__ = "problemas_por_regiao"
    __table_args__ = {"schema": "analytics"}
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    regiao: Mapped[str] = mapped_column(String(100), index=True)
    total_problemas: Mapped[int] = mapped_column(Integer)
    
class ProblemasPorStatusModel(Base):
    __tablename__ = "problemas_por_status"
    __table_args__ = {"schema": "analytics"}
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    status: Mapped[str] = mapped_column(String(30))
    quantidade: Mapped[int] = mapped_column(Integer)
    
class ProblemasPorPeriodoModel(Base):
    __tablename__ = "problemas_por_periodo"
    __table_args__ = {"schema": "analytics"}
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    data_referencia: Mapped[date] = mapped_column(Date, index=True)
    ano: Mapped[int] = mapped_column(Integer)
    mes: Mapped[int] = mapped_column(Integer)
    total_abertos: Mapped[int] = mapped_column(Integer)
    total_resolvidos: Mapped[int] = mapped_column(Integer)

class PontosWifiPorBairroModel(Base):
    __tablename__ = "pontos_wifi_por_bairro"
    __table_args__ = {"schema": "analytics"}

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    bairro: Mapped[str] = mapped_column(String(100), index=True)
    regiao: Mapped[str] = mapped_column(String(50))
    total_pontos: Mapped[int] = mapped_column(Integer)
    total_ativos: Mapped[int] = mapped_column(Integer)
    total_manutencao: Mapped[int] = mapped_column(Integer, default=0)
    total_inativos: Mapped[int] = mapped_column(Integer, default=0)