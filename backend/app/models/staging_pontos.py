from sqlalchemy import Column, Numeric, String, DateTime
from sqlalchemy.sql import func
from database.database import Base

class PontosWifiPrefeitura(Base):
    __tablename__ = "pontos_wifi_prefeitura"
    __table_args__ = {"schema": "staging"}

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
    ingested_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
