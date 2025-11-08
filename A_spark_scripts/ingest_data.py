"""
Script de Ingestão de Dados para Processamento Spark
Apêndice A - TCC: Eficiência e Escalabilidade com Cloud Computing
"""

from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, TimestampType
import sys

def create_spark_session():
    """Cria sessão Spark com configurações otimizadas."""
    return SparkSession.builder \
        .appName("BigData-Ingestion") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true") \
        .getOrCreate()

def define_schema():
    """Define schema para NYC Taxi Dataset."""
    return StructType([
        StructField("vendor_id", StringType(), True),
        StructField("pickup_datetime", TimestampType(), True),
        StructField("dropoff_datetime", TimestampType(), True),
        StructField("passenger_count", StringType(), True),
        StructField("trip_distance", DoubleType(), True),
        StructField("pickup_longitude", DoubleType(), True),
        StructField("pickup_latitude", DoubleType(), True),
        StructField("fare_amount", DoubleType(), True),
        StructField("total_amount", DoubleType(), True)
    ])

def ingest_from_s3(spark, s3_path, output_path):
    """
    Ingere dados do S3 e salva em formato Parquet otimizado.

    Args:
        spark: SparkSession
        s3_path: Caminho S3 dos dados brutos (CSV)
        output_path: Caminho S3 para salvar Parquet
    """
    schema = define_schema()

    # Leitura otimizada do S3
    df = spark.read \
        .option("header", "true") \
        .schema(schema) \
        .csv(s3_path)

    # Validação básica
    print(f"Registros lidos: {df.count()}")
    print(f"Colunas: {len(df.columns)}")

    # Salvamento em Parquet com particionamento
    df.write \
        .mode("overwrite") \
        .partitionBy("pickup_datetime") \
        .parquet(output_path)

    print(f"Dados salvos em: {output_path}")
    return df

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python ingest_data.py <s3_input> <s3_output>")
        sys.exit(1)

    spark = create_spark_session()
    ingest_from_s3(spark, sys.argv[1], sys.argv[2])
    spark.stop()
