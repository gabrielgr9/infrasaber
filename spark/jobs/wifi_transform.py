import psycopg2
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

PG_CONN = dict(
    host="postgres", port=5432, dbname="infrasaber",
    user="postgres", password="postgres123"
)
JDBC_URL = "jdbc:postgresql://postgres:5432/infrasaber"
JDBC_PROPS = {
    "user": "postgres",
    "password": "postgres123",
    "driver": "org.postgresql.Driver"
}


def get_spark():
    return (
        SparkSession.builder
        .appName("InfraSaber-WifiPrefeitura")
        .config("spark.jars.packages", "org.postgresql:postgresql:42.7.3")
        .master("local[*]")
        .getOrCreate()
    )

def truncate_targets():
    conn = psycopg2.connect(**PG_CONN)
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE trusted.pontos_wifi_prefeitura;")
        cur.execute("TRUNCATE TABLE analytics.pontos_wifi_por_bairro;")
    conn.close()


def read_staging(spark):
    return spark.read.jdbc(
        url=JDBC_URL,
        table="staging.pontos_wifi_prefeitura",
        properties=JDBC_PROPS
    )

def write_trusted(df):
    (
        df
        .withColumn("cleaned_at", F.current_timestamp())
        .write.jdbc(
            url=JDBC_URL,
            table="trusted.pontos_wifi_prefeitura",
            mode="append",
            properties=JDBC_PROPS
        )
    )


def clean(df):
    return (
        df
        .withColumn("bairro", F.initcap(F.trim(F.col("bairro"))))
        .withColumn("regiao", F.initcap(F.trim(F.col("regiao"))))
        # impa e normaliza o status de forma robusta
        .withColumn("status", F.lower(F.trim(F.col("status"))))
        .drop("ingested_at")
        .dropDuplicates(["id_ponto_externo"])
    )

def build_aggregate(df):
    df_agg = (
        df.groupBy("bairro", "regiao")
        .agg(
            F.count("*").alias("total_pontos"),
            # Ativo: apenas se tiver como 'ativo' e não 'manuten' ou 'inativo'
            F.sum(
                F.when(
                    F.col("status").contains("ativo") & 
                    ~F.col("status").contains("manuten") & 
                    ~F.col("status").contains("inativo"), 
                    1
                ).otherwise(0)
            ).alias("total_ativos"),
            # Manutenção: se contiver 'manuten'
            F.sum(
                F.when(
                    F.col("status").contains("manuten"), 
                    1
                ).otherwise(0)
            ).alias("total_manutencao"),
            # Inativo: se contiver 'inativo'
            F.sum(
                F.when(
                    (F.col("status").contains("inativo") | F.col("status").contains("desativado")) & 
                    ~F.col("status").contains("manuten"), 
                    1
                ).otherwise(0)
            ).alias("total_inativos")
        )
    )
    
    return df_agg.select(
        "bairro",
        "regiao",
        "total_pontos",
        "total_ativos",
        "total_manutencao",
        "total_inativos"
    )


def write_analytics(df_agg):
    df_agg.write.jdbc(
        url=JDBC_URL,
        table="analytics.pontos_wifi_por_bairro",
        mode="append",
        properties=JDBC_PROPS
    )


def main():
    spark = get_spark()
    truncate_targets()

    df_raw = read_staging(spark)
    df_clean = clean(df_raw)
    write_trusted(df_clean)

    df_agg = build_aggregate(df_clean)
    write_analytics(df_agg)

    print(f"Concluído: {df_clean.count()} pontos tratados, {df_agg.count()} bairros agregados.")
    spark.stop()


if __name__ == "__main__":
    main()