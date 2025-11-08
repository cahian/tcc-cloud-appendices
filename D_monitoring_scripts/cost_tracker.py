"""
Rastreador de Custos AWS
Apêndice D - TCC: Eficiência e Escalabilidade com Cloud Computing
"""

from datetime import datetime, timedelta

class CostTracker:
    """Rastreia e calcula custos de infraestrutura AWS."""

    # Preços por hora (região us-east-1, aproximados)
    INSTANCE_PRICES = {
        'm5.xlarge': {'on_demand': 0.192, 'spot': 0.077},
        'c5.2xlarge': {'on_demand': 0.340, 'spot': 0.136},
        'm5.2xlarge': {'on_demand': 0.384, 'spot': 0.154},
    }

    S3_PRICE_PER_GB = 0.023  # $/GB/mês
    DATA_TRANSFER_PRICE = 0.09  # $/GB

    def __init__(self):
        self.cost_history = []

    def calculate_cluster_cost(self, instance_type, count, hours, use_spot=False):
        """
        Calcula custo de um cluster EMR.

        Args:
            instance_type: Tipo de instância EC2
            count: Número de instâncias
            hours: Horas de execução
            use_spot: Se True, usa preço spot; senão on-demand

        Returns:
            Custo total em dólares
        """
        price_type = 'spot' if use_spot else 'on_demand'
        hourly_price = self.INSTANCE_PRICES.get(instance_type, {}).get(price_type, 0)

        instance_cost = hourly_price * count * hours
        emr_fee = instance_cost * 0.25  # EMR cobra 25% adicional

        total_cost = instance_cost + emr_fee

        return {
            'instance_cost': instance_cost,
            'emr_fee': emr_fee,
            'total_cost': total_cost,
            'hourly_rate': hourly_price,
            'instances': count,
            'hours': hours
        }

    def calculate_job_cost(self, master_type, worker_type, worker_count,
                          duration_hours, data_processed_gb, use_spot=False):
        """
        Calcula custo completo de um job de processamento.

        Args:
            master_type: Tipo de instância do master
            worker_type: Tipo de instância dos workers
            worker_count: Número de workers
            duration_hours: Duração em horas
            data_processed_gb: Dados processados em GB
            use_spot: Usar spot instances

        Returns:
            Breakdown detalhado de custos
        """
        # Custo do master
        master_cost = self.calculate_cluster_cost(
            master_type, 1, duration_hours, use_spot=False
        )

        # Custo dos workers
        worker_cost = self.calculate_cluster_cost(
            worker_type, worker_count, duration_hours, use_spot
        )

        # Custo de armazenamento S3
        storage_cost = data_processed_gb * self.S3_PRICE_PER_GB / 30  # Pro-rata diário

        # Custo de transferência de dados
        transfer_cost = data_processed_gb * self.DATA_TRANSFER_PRICE

        total = (master_cost['total_cost'] +
                worker_cost['total_cost'] +
                storage_cost +
                transfer_cost)

        cost_per_gb = total / data_processed_gb if data_processed_gb > 0 else 0

        return {
            'master_cost': master_cost['total_cost'],
            'worker_cost': worker_cost['total_cost'],
            'storage_cost': storage_cost,
            'transfer_cost': transfer_cost,
            'total_cost': total,
            'cost_per_gb': cost_per_gb,
            'data_processed_gb': data_processed_gb,
            'use_spot': use_spot
        }

    def compare_spot_vs_ondemand(self, worker_type, worker_count, duration_hours, data_gb):
        """Compara custos entre spot e on-demand."""
        print(f"\n{'='*60}")
        print("COMPARAÇÃO: SPOT vs ON-DEMAND")
        print(f"{'='*60}\n")

        ondemand = self.calculate_job_cost(
            'm5.xlarge', worker_type, worker_count,
            duration_hours, data_gb, use_spot=False
        )

        spot = self.calculate_job_cost(
            'm5.xlarge', worker_type, worker_count,
            duration_hours, data_gb, use_spot=True
        )

        savings = ondemand['total_cost'] - spot['total_cost']
        savings_pct = (savings / ondemand['total_cost']) * 100

        print(f"Configuração:")
        print(f"  • Workers: {worker_count}x {worker_type}")
        print(f"  • Duração: {duration_hours} horas")
        print(f"  • Dados: {data_gb} GB\n")

        print(f"On-Demand:")
        print(f"  • Custo total: ${ondemand['total_cost']:.2f}")
        print(f"  • Custo/GB: ${ondemand['cost_per_gb']:.4f}\n")

        print(f"Spot Instances:")
        print(f"  • Custo total: ${spot['total_cost']:.2f}")
        print(f"  • Custo/GB: ${spot['cost_per_gb']:.4f}\n")

        print(f"💰 Economia: ${savings:.2f} ({savings_pct:.1f}%)")

        return {'ondemand': ondemand, 'spot': spot, 'savings': savings}

    def estimate_monthly_cost(self, daily_jobs=1, avg_duration_hours=2,
                             avg_data_gb=100, worker_count=4):
        """Estima custo mensal baseado em uso diário."""
        daily_cost = self.calculate_job_cost(
            'm5.xlarge', 'c5.2xlarge', worker_count,
            avg_duration_hours, avg_data_gb, use_spot=True
        )

        monthly_cost = daily_cost['total_cost'] * daily_jobs * 30

        print(f"\n{'='*60}")
        print("ESTIMATIVA DE CUSTO MENSAL")
        print(f"{'='*60}\n")
        print(f"Premissas:")
        print(f"  • Jobs por dia: {daily_jobs}")
        print(f"  • Duração média: {avg_duration_hours}h")
        print(f"  • Dados por job: {avg_data_gb}GB")
        print(f"  • Workers: {worker_count}x c5.2xlarge (spot)\n")
        print(f"Custos:")
        print(f"  • Por job: ${daily_cost['total_cost']:.2f}")
        print(f"  • Por dia: ${daily_cost['total_cost'] * daily_jobs:.2f}")
        print(f"  • Por mês: ${monthly_cost:.2f}")

        return monthly_cost


def main():
    """Demonstração do rastreador de custos."""
    tracker = CostTracker()

    # Cenário 1: Job típico
    print("CENÁRIO 1: Job de processamento típico")
    job_cost = tracker.calculate_job_cost(
        master_type='m5.xlarge',
        worker_type='c5.2xlarge',
        worker_count=4,
        duration_hours=1.5,
        data_processed_gb=100,
        use_spot=True
    )
    print(f"\nCusto total: ${job_cost['total_cost']:.2f}")
    print(f"Custo por GB: ${job_cost['cost_per_gb']:.4f}")

    # Cenário 2: Spot vs On-Demand
    tracker.compare_spot_vs_ondemand(
        worker_type='c5.2xlarge',
        worker_count=4,
        duration_hours=2,
        data_gb=250
    )

    # Cenário 3: Estimativa mensal
    tracker.estimate_monthly_cost(
        daily_jobs=2,
        avg_duration_hours=1.5,
        avg_data_gb=150,
        worker_count=4
    )


if __name__ == "__main__":
    main()
