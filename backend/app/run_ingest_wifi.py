import sys
from database.database import SessionLocal
from services.wifi_prefeitura_service import WifiPrefeituraService

if __name__ == "__main__":
    caminho = sys.argv[1] if len(sys.argv) > 1 else "/code/data/brutos/pontos_internet_carapicuiba_400.csv"
    db = SessionLocal()
    try:
        total = WifiPrefeituraService(db).ingest_csv_staging(caminho_csv=caminho)
        print(f"OK: {total} registros inseridos no staging.")
    finally:
        db.close()