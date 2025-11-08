"""
Utilitários de Otimização Spark
Apêndice A - TCC: Eficiência e Escalabilidade com Cloud Computing
"""

from pyspark.sql import SparkSession

class SparkOptimizer:
    """Classe com configurações otimizadas para diferentes cargas de trabalho."""

    @staticmethod
    def get_optimized_session(workload_type="balanced"):
        """
        Cria sessão Spark otimizada para diferentes tipos de carga.

        Args:
            workload_type: "balanced", "memory_intensive", "cpu_intensive"
        """
        configs = {
            "balanced": {
                "spark.executor.memory": "12g",
                "spark.executor.cores": "4",
                "spark.sql.shuffle.partitions": "200"
            },
            "memory_intensive": {
                "spark.executor.memory": "16g",
                "spark.executor.cores": "2",
                "spark.memory.fraction": "0.8",
                "spark.sql.shuffle.partitions": "100"
            },
            "cpu_intensive": {
                "spark.executor.memory": "8g",
                "spark.executor.cores": "8",
                "spark.sql.shuffle.partitions": "400"
            }
        }

        builder = SparkSession.builder \
            .appName(f"BigData-{workload_type}") \
            .config("spark.sql.adaptive.enabled", "true") \
            .config("spark.dynamicAllocation.enabled", "true")

        # Aplica configurações específicas
        for key, value in configs[workload_type].items():
            builder = builder.config(key, value)

        return builder.getOrCreate()

    @staticmethod
    def enable_broadcast_join(df, threshold_mb=10):
        """Habilita broadcast join para tabelas pequenas."""
        spark = df.sparkSession
        spark.conf.set("spark.sql.autoBroadcastJoinThreshold", threshold_mb * 1024 * 1024)
        return df

    @staticmethod
    def optimize_partitions(df, target_size_mb=128):
        """Otimiza número de partições baseado no tamanho dos dados."""
        spark = df.sparkSession
        num_partitions = max(int(df.count() / 1000000), 1) * 10
        spark.conf.set("spark.sql.shuffle.partitions", str(num_partitions))
        return df.repartition(num_partitions)

# Exemplo de uso
if __name__ == "__main__":
    # Criar sessão otimizada
    spark = SparkOptimizer.get_optimized_session("balanced")

    print("Configurações aplicadas:")
    print(f"- Executor Memory: {spark.conf.get('spark.executor.memory')}")
    print(f"- Executor Cores: {spark.conf.get('spark.executor.cores')}")
    print(f"- Adaptive Execution: {spark.conf.get('spark.sql.adaptive.enabled')}")

    spark.stop()
