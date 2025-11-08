"""
Monitoramento contínuo de clusters EMR
Apêndice D - TCC: Eficiência e Escalabilidade com Cloud Computing
"""

from __future__ import annotations

import argparse
import sys
import time
from datetime import datetime, timedelta
from typing import Dict, Optional

try:
    import boto3
except ImportError:  # pragma: no cover
    boto3 = None


class ClusterMonitor:
    """Monitora status de clusters EMR e publica métricas básicas."""

    def __init__(self, region: str = "us-east-1", dry_run: bool = False):
        self.region = region
        self.dry_run = dry_run or boto3 is None

        if not self.dry_run:
            self.emr = boto3.client("emr", region_name=region)
            self.cloudwatch = boto3.client("cloudwatch", region_name=region)
        else:
            self.emr = None
            self.cloudwatch = None

    def describe_cluster(self, cluster_id: str) -> Dict[str, str]:
        """Recupera status atual do cluster."""
        if self.dry_run:
            return {
                "State": "WAITING",
                "StateChangeReason": "dry-run mode",
                "MasterPublicDnsName": "dry-run.emr.aws",
            }

        response = self.emr.describe_cluster(ClusterId=cluster_id)
        cluster = response["Cluster"]
        return {
            "State": cluster["Status"]["State"],
            "StateChangeReason": cluster["Status"]["StateChangeReason"]["Message"],
            "MasterPublicDnsName": cluster.get("MasterPublicDnsName", "n/a"),
        }

    def fetch_metric(
        self,
        cluster_id: str,
        metric_name: str = "AppsRunning",
        period_seconds: int = 300,
    ) -> Optional[float]:
        """Busca métrica agregada no CloudWatch."""
        if self.dry_run:
            # Valores fictícios para documentação/testes
            return 3.0 if metric_name == "AppsRunning" else 70.0

        end_time = datetime.utcnow()
        start_time = end_time - timedelta(seconds=period_seconds)

        response = self.cloudwatch.get_metric_statistics(
            Namespace="AWS/ElasticMapReduce",
            MetricName=metric_name,
            Dimensions=[{"Name": "JobFlowId", "Value": cluster_id}],
            StartTime=start_time,
            EndTime=end_time,
            Period=period_seconds,
            Statistics=["Average"],
        )

        datapoints = response.get("Datapoints", [])
        if not datapoints:
            return None

        # Usa o datapoint mais recente
        datapoints.sort(key=lambda point: point["Timestamp"])
        return datapoints[-1]["Average"]

    def monitor(
        self,
        cluster_id: str,
        interval_seconds: int = 30,
        timeout_minutes: int = 60,
    ) -> None:
        """Loop principal de monitoramento."""
        start_time = time.time()
        print(f"Monitorando cluster {cluster_id} (region={self.region}, dry_run={self.dry_run})")
        print("-" * 80)

        while True:
            elapsed = time.time() - start_time
            if elapsed > timeout_minutes * 60:
                print("Tempo máximo de monitoramento atingido; encerrando.")
                break

            status = self.describe_cluster(cluster_id)
            apps_running = self.fetch_metric(cluster_id, "AppsRunning")
            yarn_memory = self.fetch_metric(cluster_id, "YARNMemoryAvailablePercentage")

            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"[{timestamp}] Estado: {status['State']}")
            print(f"  Motivo: {status['StateChangeReason']}")
            print(f"  Master DNS: {status['MasterPublicDnsName']}")

            if apps_running is not None:
                print(f"  Apps em execução: {apps_running:.1f}")
            if yarn_memory is not None:
                print(f"  YARN Memory disponível: {yarn_memory:.1f}%")

            if status["State"] in {"TERMINATED", "TERMINATED_WITH_ERRORS"}:
                print(f"Cluster finalizado com estado {status['State']}.")
                break

            time.sleep(interval_seconds)


def parse_args(argv: Optional[list[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Monitor de clusters EMR")
    parser.add_argument("--cluster-id", required=True, help="ID do cluster EMR (ex: j-XXXXXXXX)")
    parser.add_argument("--region", default="us-east-1", help="Região AWS (padrão: us-east-1)")
    parser.add_argument("--interval", type=int, default=30, help="Intervalo entre leituras (s)")
    parser.add_argument("--timeout", type=int, default=60, help="Tempo máximo em minutos")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simula respostas para testes locais sem credenciais AWS",
    )
    return parser.parse_args(argv)


def main(argv: Optional[list[str]] = None) -> None:
    args = parse_args(argv)
    monitor = ClusterMonitor(region=args.region, dry_run=args.dry_run)
    monitor.monitor(
        cluster_id=args.cluster_id,
        interval_seconds=args.interval,
        timeout_minutes=args.timeout,
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nMonitoramento interrompido pelo usuário.")
    except Exception as exc:  # pragma: no cover - log básico para o apêndice
        print(f"Erro ao monitorar cluster: {exc}")
        sys.exit(1)
