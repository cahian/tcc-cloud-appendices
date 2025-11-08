"""
Coletor de Métricas CloudWatch
Apêndice D - TCC: Eficiência e Escalabilidade com Cloud Computing
"""

import boto3
from datetime import datetime, timedelta
import time

class CloudWatchMetricsCollector:
    """Coleta e publica métricas no CloudWatch."""

    def __init__(self, region='us-east-1'):
        self.cloudwatch = boto3.client('cloudwatch', region_name=region)
        self.namespace = 'BigData/EMR'

    def publish_metric(self, metric_name, value, unit='None', dimensions=None):
        """
        Publica uma métrica no CloudWatch.

        Args:
            metric_name: Nome da métrica
            value: Valor numérico
            unit: Unidade (Count, Bytes, Seconds, etc.)
            dimensions: Dict com dimensões adicionais
        """
        metric_data = {
            'MetricName': metric_name,
            'Value': value,
            'Unit': unit,
            'Timestamp': datetime.utcnow()
        }

        if dimensions:
            metric_data['Dimensions'] = [
                {'Name': k, 'Value': v} for k, v in dimensions.items()
            ]

        try:
            self.cloudwatch.put_metric_data(
                Namespace=self.namespace,
                MetricData=[metric_data]
            )
            print(f"✓ Métrica publicada: {metric_name} = {value} {unit}")
        except Exception as e:
            print(f"✗ Erro ao publicar {metric_name}: {e}")

    def get_cluster_metrics(self, cluster_id, metric_name, period=300):
        """
        Recupera métricas de um cluster EMR.

        Args:
            cluster_id: ID do cluster EMR
            metric_name: Nome da métrica (ex: YARNMemoryAvailablePercentage)
            period: Período em segundos (padrão: 5 minutos)
        """
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=1)

        response = self.cloudwatch.get_metric_statistics(
            Namespace='AWS/ElasticMapReduce',
            MetricName=metric_name,
            Dimensions=[
                {'Name': 'JobFlowId', 'Value': cluster_id}
            ],
            StartTime=start_time,
            EndTime=end_time,
            Period=period,
            Statistics=['Average', 'Maximum']
        )

        datapoints = sorted(response['Datapoints'], key=lambda x: x['Timestamp'])
        return datapoints

    def monitor_performance(self, job_id, duration_seconds):
        """
        Monitora performance de um job Spark.

        Args:
            job_id: ID do job
            duration_seconds: Duração da execução
        """
        # Métricas simuladas (em produção, viriam do Spark)
        metrics = {
            'ExecutionTime': (duration_seconds, 'Seconds'),
            'RecordsProcessed': (1500000, 'Count'),
            'DataProcessed': (250, 'Gigabytes'),
            'CPUUtilization': (72.5, 'Percent'),
            'MemoryUtilization': (68.3, 'Percent'),
        }

        dimensions = {'JobId': job_id, 'Environment': 'production'}

        for metric_name, (value, unit) in metrics.items():
            self.publish_metric(metric_name, value, unit, dimensions)

        # Calcular throughput
        throughput = (250 / duration_seconds) * 3600  # GB/hora
        self.publish_metric('Throughput', throughput, 'Gigabytes/Hour', dimensions)


def main():
    """Exemplo de uso do coletor de métricas."""
    collector = CloudWatchMetricsCollector()

    # Simular monitoramento de um job
    print("Iniciando monitoramento de performance...\n")

    job_id = f"spark-job-{int(time.time())}"
    execution_time = 1850  # segundos (~30 minutos)

    collector.monitor_performance(job_id, execution_time)

    print(f"\nMonitoramento concluído para job: {job_id}")
    print("Métricas disponíveis no CloudWatch!")


if __name__ == "__main__":
    main()
