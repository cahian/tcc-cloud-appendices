"""
Suite de Benchmarks de Performance
Apêndice D - TCC: Eficiência e Escalabilidade com Cloud Computing
"""

import time
import statistics
from datetime import datetime

class BenchmarkSuite:
    """Suite completa de testes de performance."""

    def __init__(self):
        self.results = []

    def measure_throughput(self, dataset_size_gb, processing_time_seconds):
        """
        Calcula throughput de processamento.

        Args:
            dataset_size_gb: Tamanho do dataset em GB
            processing_time_seconds: Tempo de processamento em segundos

        Returns:
            dict com métricas de throughput
        """
        throughput_gb_hour = (dataset_size_gb / processing_time_seconds) * 3600
        throughput_mb_sec = (dataset_size_gb * 1024) / processing_time_seconds

        return {
            'dataset_gb': dataset_size_gb,
            'time_seconds': processing_time_seconds,
            'throughput_gb_hour': throughput_gb_hour,
            'throughput_mb_sec': throughput_mb_sec,
            'timestamp': datetime.now().isoformat()
        }

    def run_scalability_test(self, cluster_sizes, dataset_size=100):
        """
        Testa escalabilidade com diferentes tamanhos de cluster.

        Args:
            cluster_sizes: Lista de tamanhos de cluster (número de nodes)
            dataset_size: Tamanho do dataset em GB
        """
        print(f"\n{'='*60}")
        print(f"TESTE DE ESCALABILIDADE - Dataset: {dataset_size}GB")
        print(f"{'='*60}\n")

        results = []

        for nodes in cluster_sizes:
            print(f"Testando com {nodes} nodes...")

            # Simula tempo de processamento (inversamente proporcional ao número de nodes)
            base_time = 3600  # 1 hora para 1 node
            processing_time = base_time / (nodes * 0.8)  # Eficiência de 80%

            result = self.measure_throughput(dataset_size, processing_time)
            result['cluster_nodes'] = nodes
            results.append(result)

            print(f"  ✓ Tempo: {processing_time:.1f}s")
            print(f"  ✓ Throughput: {result['throughput_gb_hour']:.2f} GB/hora\n")

        self.results.extend(results)
        return results

    def calculate_statistics(self, results):
        """Calcula estatísticas dos resultados."""
        throughputs = [r['throughput_gb_hour'] for r in results]

        return {
            'mean': statistics.mean(throughputs),
            'median': statistics.median(throughputs),
            'stdev': statistics.stdev(throughputs) if len(throughputs) > 1 else 0,
            'min': min(throughputs),
            'max': max(throughputs),
            'samples': len(throughputs)
        }

    def compare_technologies(self):
        """
        Compara performance entre diferentes tecnologias.
        Baseado nos resultados do TCC.
        """
        print(f"\n{'='*60}")
        print("COMPARAÇÃO DE TECNOLOGIAS - Dataset 100GB")
        print(f"{'='*60}\n")

        # Dados baseados no TCC
        technologies = {
            'Hadoop MapReduce': 7200,   # 2 horas
            'Apache Spark': 4680,        # 1.3 horas (35% mais rápido)
            'Google BigQuery': 3456,     # 0.96 horas (108% mais rápido que Hadoop)
        }

        results = []
        for tech, time_seconds in technologies.items():
            result = self.measure_throughput(100, time_seconds)
            result['technology'] = tech
            results.append(result)

            speedup = technologies['Hadoop MapReduce'] / time_seconds
            print(f"{tech}:")
            print(f"  • Tempo: {time_seconds/3600:.2f} horas")
            print(f"  • Throughput: {result['throughput_gb_hour']:.2f} GB/hora")
            print(f"  • Speedup: {speedup:.2f}x\n")

        return results

    def generate_report(self):
        """Gera relatório consolidado dos benchmarks."""
        if not self.results:
            print("Nenhum resultado disponível.")
            return

        print(f"\n{'='*60}")
        print("RELATÓRIO DE BENCHMARKS")
        print(f"{'='*60}\n")

        stats = self.calculate_statistics(self.results)

        print(f"Total de testes executados: {stats['samples']}")
        print(f"\nThroughput (GB/hora):")
        print(f"  • Média: {stats['mean']:.2f}")
        print(f"  • Mediana: {stats['median']:.2f}")
        print(f"  • Desvio Padrão: {stats['stdev']:.2f}")
        print(f"  • Mínimo: {stats['min']:.2f}")
        print(f"  • Máximo: {stats['max']:.2f}")


def main():
    """Executa suite completa de benchmarks."""
    suite = BenchmarkSuite()

    # Teste 1: Escalabilidade
    cluster_sizes = [2, 4, 8, 16]
    suite.run_scalability_test(cluster_sizes, dataset_size=100)

    # Teste 2: Comparação de tecnologias
    suite.compare_technologies()

    # Relatório final
    suite.generate_report()


if __name__ == "__main__":
    main()
