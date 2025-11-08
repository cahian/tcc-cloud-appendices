"""
DAG para Testes de Escalabilidade
Apêndice C - TCC: Eficiência e Escalabilidade com Cloud Computing

Nota: As tasks utilizam simulação (`time.sleep`) para permitir execução local
sem provisionar clusters reais. Substitua por operadores EMR conforme necessário.
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.operators.emr import EmrAddStepsOperator
import time

default_args = {
    'owner': 'bigdata-team',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def run_benchmark(dataset_size, **context):
    """Simula execução de benchmark com diferentes tamanhos de dados."""
    print(f"Iniciando benchmark com dataset de {dataset_size}GB...")
    start_time = time.time()

    # Aqui entraria a lógica real de benchmark
    time.sleep(2)  # Simula processamento

    execution_time = time.time() - start_time
    throughput = dataset_size / (execution_time / 3600)  # GB/hora

    print(f"Benchmark concluído!")
    print(f"- Dataset: {dataset_size}GB")
    print(f"- Tempo: {execution_time:.2f}s")
    print(f"- Throughput: {throughput:.2f} GB/hora")

    return {
        'dataset_size': dataset_size,
        'execution_time': execution_time,
        'throughput': throughput
    }

def aggregate_results(**context):
    """Agrega resultados de todos os benchmarks."""
    print("Agregando resultados dos benchmarks...")
    # Recupera resultados das tasks anteriores via XCom
    ti = context['task_instance']

    results = []
    for size in [100, 500, 1000]:
        result = ti.xcom_pull(task_ids=f'benchmark_{size}gb')
        if result:
            results.append(result)

    print(f"Total de benchmarks executados: {len(results)}")
    return results

with DAG(
    'scalability_testing',
    default_args=default_args,
    description='Testes automatizados de escalabilidade',
    schedule_interval='@weekly',
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['bigdata', 'benchmark', 'testing'],
) as dag:

    # Benchmarks com diferentes tamanhos
    benchmark_100gb = PythonOperator(
        task_id='benchmark_100gb',
        python_callable=run_benchmark,
        op_kwargs={'dataset_size': 100},
    )

    benchmark_500gb = PythonOperator(
        task_id='benchmark_500gb',
        python_callable=run_benchmark,
        op_kwargs={'dataset_size': 500},
    )

    benchmark_1tb = PythonOperator(
        task_id='benchmark_1000gb',
        python_callable=run_benchmark,
        op_kwargs={'dataset_size': 1000},
    )

    # Agregação de resultados
    aggregate = PythonOperator(
        task_id='aggregate_results',
        python_callable=aggregate_results,
    )

    # Executar benchmarks em paralelo, depois agregar
    [benchmark_100gb, benchmark_500gb, benchmark_1tb] >> aggregate
