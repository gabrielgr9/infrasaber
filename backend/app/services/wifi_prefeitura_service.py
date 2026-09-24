import pandas as pd
from sqlalchemy.orm import Session
from models.staging_pontos import PontosWifiPrefeitura

class WifiPrefeituraService:
    def __init__(self, db: Session):
        self.db = db
        
    def ingest_csv_staging(self, caminho_csv: str = "data/brutos/pontos_internet_carapicuiba_400.csv") -> int:
        print(f"Lendo o arquivo bruto em: {caminho_csv}")
        df = pd.read_csv(caminho_csv)
        contador = 0
        
        try:
            for _, row in df.iterrows():
                link_val = row['link'] if pd.notna(row['link']) else None
                
                ponto = PontosWifiPrefeitura(
                    id_ponto_externo=str(row['id_ponto_externo']),
                    nome_local=str(row['nome_local']),
                    tipo=str(row['tipo']),
                    endereco=str(row['endereco']),
                    bairro=str(row['bairro']),
                    subprefeitura=str(row['subprefeitura']),
                    regiao=str(row['regiao']),
                    latitude=float(row['latitude']),
                    longitude=float(row['longitude']),
                    status=str(row['status']),
                    horario_funcionamento=str(row['horario_funcionamento']),
                    descricao=str(row['descricao']),
                    link=link_val
                )
                self.db.merge(ponto)
                contador += 1
            self.db.commit()
            print(f"Carga de staging foi concluída com sucesso! O total de registros procssados: {contador}")
            return contador
        
        except Exception as e:
            self.db.rollback()
            print(f"Erro durante o processo de ingestão: {e}")
            raise