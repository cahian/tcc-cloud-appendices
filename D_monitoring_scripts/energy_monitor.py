"""
Monitor de Eficiência Energética
Apêndice D - TCC: Eficiência e Escalabilidade com Cloud Computing
"""

class EnergyMonitor:
    """Monitora e calcula eficiência energética do processamento."""

    # Consumo médio por tipo de instância (kWh)
    INSTANCE_POWER = {
        'm5.xlarge': 0.08,    # ~80W
        'c5.2xlarge': 0.15,   # ~150W
        'm5.2xlarge': 0.12,   # ~120W
    }

    # Fator de eficiência do datacenter (PUE - Power Usage Effectiveness)
    # AWS geralmente tem PUE entre 1.1-1.2
    PUE = 1.15

    # Emissões de CO2 por região (kg CO2/kWh)
    CO2_EMISSIONS = {
        'us-east-1': 0.385,      # Virginia (mix energético)
        'us-west-1': 0.219,      # Califórnia (mais renovável)
        'eu-west-1': 0.312,      # Irlanda
        'sa-east-1': 0.098,      # São Paulo (hidrelétrica)
    }

    def __init__(self, region='us-east-1'):
        self.region = region
        self.co2_factor = self.CO2_EMISSIONS.get(region, 0.385)

    def calculate_energy_consumption(self, instance_type, count, hours):
        """
        Calcula consumo de energia de um cluster.

        Args:
            instance_type: Tipo de instância
            count: Número de instâncias
            hours: Horas de execução

        Returns:
            Consumo em kWh
        """
        instance_power = self.INSTANCE_POWER.get(instance_type, 0.1)
        base_consumption = instance_power * count * hours
        total_consumption = base_consumption * self.PUE

        return {
            'base_kwh': base_consumption,
            'total_kwh': total_consumption,
            'pue': self.PUE,
            'instances': count,
            'hours': hours
        }

    def calculate_carbon_footprint(self, energy_kwh):
        """
        Calcula pegada de carbono.

        Args:
            energy_kwh: Energia consumida em kWh

        Returns:
            Emissões em kg CO2
        """
        co2_kg = energy_kwh * self.co2_factor

        return {
            'co2_kg': co2_kg,
            'co2_tons': co2_kg / 1000,
            'region': self.region,
            'emission_factor': self.co2_factor
        }

    def calculate_efficiency_metrics(self, data_processed_tb, energy_kwh):
        """
        Calcula métricas de eficiência energética.

        Args:
            data_processed_tb: Dados processados em TB
            energy_kwh: Energia consumida em kWh

        Returns:
            Métricas de eficiência
        """
        kwh_per_tb = energy_kwh / data_processed_tb if data_processed_tb > 0 else 0
        tb_per_kwh = data_processed_tb / energy_kwh if energy_kwh > 0 else 0

        co2 = self.calculate_carbon_footprint(energy_kwh)
        co2_per_tb = co2['co2_kg'] / data_processed_tb if data_processed_tb > 0 else 0

        return {
            'kwh_per_tb': kwh_per_tb,
            'tb_per_kwh': tb_per_kwh,
            'co2_kg_per_tb': co2_per_tb,
            'total_co2_kg': co2['co2_kg'],
            'data_processed_tb': data_processed_tb,
            'energy_kwh': energy_kwh
        }

    def job_energy_report(self, master_type, worker_type, worker_count,
                         duration_hours, data_processed_gb):
        """
        Gera relatório completo de energia para um job.

        Args:
            master_type: Tipo do master
            worker_type: Tipo dos workers
            worker_count: Número de workers
            duration_hours: Duração em horas
            data_processed_gb: Dados processados em GB
        """
        print(f"\n{'='*60}")
        print("RELATÓRIO DE EFICIÊNCIA ENERGÉTICA")
        print(f"{'='*60}\n")

        # Consumo do master
        master_energy = self.calculate_energy_consumption(
            master_type, 1, duration_hours
        )

        # Consumo dos workers
        worker_energy = self.calculate_energy_consumption(
            worker_type, worker_count, duration_hours
        )

        # Total
        total_energy = master_energy['total_kwh'] + worker_energy['total_kwh']
        data_tb = data_processed_gb / 1024

        # Métricas
        efficiency = self.calculate_efficiency_metrics(data_tb, total_energy)
        carbon = self.calculate_carbon_footprint(total_energy)

        print(f"Configuração:")
        print(f"  • Master: 1x {master_type}")
        print(f"  • Workers: {worker_count}x {worker_type}")
        print(f"  • Duração: {duration_hours:.2f} horas")
        print(f"  • Dados: {data_processed_gb} GB ({data_tb:.2f} TB)\n")

        print(f"Consumo de Energia:")
        print(f"  • Master: {master_energy['total_kwh']:.3f} kWh")
        print(f"  • Workers: {worker_energy['total_kwh']:.3f} kWh")
        print(f"  • Total: {total_energy:.3f} kWh")
        print(f"  • PUE: {self.PUE}\n")

        print(f"Eficiência:")
        print(f"  • kWh/TB: {efficiency['kwh_per_tb']:.3f}")
        print(f"  • TB/kWh: {efficiency['tb_per_kwh']:.3f}\n")

        print(f"Pegada de Carbono:")
        print(f"  • Total: {carbon['co2_kg']:.2f} kg CO₂")
        print(f"  • Por TB: {efficiency['co2_kg_per_tb']:.2f} kg CO₂/TB")
        print(f"  • Região: {self.region}")

        return efficiency

    def compare_regions(self, instance_type, count, hours, data_tb):
        """Compara eficiência energética entre regiões."""
        print(f"\n{'='*60}")
        print("COMPARAÇÃO DE REGIÕES - Pegada de Carbono")
        print(f"{'='*60}\n")

        results = {}
        for region, co2_factor in self.CO2_EMISSIONS.items():
            monitor = EnergyMonitor(region)
            energy = monitor.calculate_energy_consumption(instance_type, count, hours)
            carbon = monitor.calculate_carbon_footprint(energy['total_kwh'])

            results[region] = carbon

            print(f"{region}:")
            print(f"  • Energia: {energy['total_kwh']:.2f} kWh")
            print(f"  • CO₂: {carbon['co2_kg']:.2f} kg")
            print(f"  • Fator: {co2_factor} kg CO₂/kWh\n")

        # Encontrar região mais eficiente
        best_region = min(results.keys(), key=lambda r: results[r]['co2_kg'])
        worst_region = max(results.keys(), key=lambda r: results[r]['co2_kg'])

        reduction = results[worst_region]['co2_kg'] - results[best_region]['co2_kg']
        reduction_pct = (reduction / results[worst_region]['co2_kg']) * 100

        print(f"🌱 Melhor região: {best_region} ({results[best_region]['co2_kg']:.2f} kg CO₂)")
        print(f"⚠️  Pior região: {worst_region} ({results[worst_region]['co2_kg']:.2f} kg CO₂)")
        print(f"💚 Redução potencial: {reduction:.2f} kg CO₂ ({reduction_pct:.1f}%)")


def main():
    """Demonstração do monitor de energia."""
    monitor = EnergyMonitor(region='us-east-1')

    # Cenário 1: Job típico
    print("CENÁRIO 1: Análise de job típico")
    monitor.job_energy_report(
        master_type='m5.xlarge',
        worker_type='c5.2xlarge',
        worker_count=4,
        duration_hours=1.5,
        data_processed_gb=250
    )

    # Cenário 2: Comparação entre regiões
    monitor.compare_regions(
        instance_type='c5.2xlarge',
        count=8,
        hours=2,
        data_tb=0.5
    )


if __name__ == "__main__":
    main()
