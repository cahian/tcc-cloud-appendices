"""
Script de Processamento ETL com PySpark
Apêndice A - TCC: Eficiência e Escalabilidade com Cloud Computing
"""

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, avg, sum, count, hour, dayofweek
import sys

def create_spark_session():
    """Cria sessão Spark com configurações de performance."""
    return SparkSession.builder \
        .appName("BigData-ETL-Processing") \
        .config("spark.executor.memory", "12g") \
        .config("spark.executor.cores", "4") \
        .config("spark.sql.adaptive.enabled", "true") \
        .config("spark.dynamicAllocation.enabled", "true") \
        .getOrCreate()

def process_taxi_data(spark, input_path, output_path):
    """
    Processa dados de táxi NYC com agregações e transformações.

    Análises:
    - Receita média por hora do dia
    - Distância média por dia da semana
    - Total de corridas por região
    """
    # Leitura dos dados em Parquet
    df = spark.read.parquet(input_path)

    # Cache para operações iterativas
    df.cache()

    # Transformações
    df_processed = df \
        .filter(col("fare_amount") > 0) \
        .filter(col("trip_distance") > 0) \
        .withColumn("pickup_hour", hour(col("pickup_datetime"))) \
        .withColumn("pickup_day", dayofweek(col("pickup_datetime")))

    # Agregação 1: Receita média por hora
    revenue_by_hour = df_processed.groupBy("pickup_hour") \
        .agg(
            avg("fare_amount").alias("avg_fare"),
            count("*").alias("trip_count"),
            sum("total_amount").alias("total_revenue")
        ) \
        .orderBy("pickup_hour")

    # Agregação 2: Estatísticas por dia da semana
    stats_by_day = df_processed.groupBy("pickup_day") \
        .agg(
            avg("trip_distance").alias("avg_distance"),
            avg("fare_amount").alias("avg_fare"),
            count("*").alias("total_trips")
        ) \
        .orderBy("pickup_day")

    # Salvar resultados
    revenue_by_hour.write.mode("overwrite").parquet(f"{output_path}/revenue_by_hour")
    stats_by_day.write.mode("overwrite").parquet(f"{output_path}/stats_by_day")

    # Métricas
    total_records = df_processed.count()
    print(f"Total de registros processados: {total_records}")
    print(f"Resultados salvos em: {output_path}")

    df.unpersist()
    return total_records

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Uso: python process_data.py <input_parquet> <output_path>")
        sys.exit(1)

    spark = create_spark_session()
    process_taxi_data(spark, sys.argv[1], sys.argv[2])
    spark.stop()
