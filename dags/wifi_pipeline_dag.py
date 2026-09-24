from datetime import datetime
from airflow import DAG
from airflow.operators.bash import BashOperator

default_args = {"owner": "infrasaber", "retries": 0}

with DAG(
    dag_id="wifi_livre_sp_pipeline",
    default_args=default_args,
    description="Extração do CSV, transformação com PySpark e carga em trusted/analytics",
    schedule_interval="@daily",
    start_date=datetime(2026, 9, 1),
    catchup=False,
    tags=["infrasaber", "wifi"],
) as dag:

    extrair_ingerir = BashOperator(
        task_id="extrair_ingerir_csv",
        bash_command=(
            "cd /opt/airflow/backend_app && "
            "python run_ingest_wifi.py /opt/airflow/data/brutos/pontos_internet_carapicuiba_400.csv"
        ),
    )

    transformar_spark = BashOperator(
        task_id="transformar_pyspark",
        bash_command="python /opt/airflow/spark_jobs/wifi_transform.py",
    )

    extrair_ingerir >> transformar_spark