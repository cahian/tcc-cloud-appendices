"""
DAG de Monitoramento e Alertas
Apêndice C - TCC: Eficiência e Escalabilidade com Cloud Computing

Nota: As métricas são mockadas para documentação/demonstração. Em produção,
substitua pelos hooks/conectores AWS correspondentes.
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.base_aws import AwsBaseHook
import boto3

default_args = {
    'owner': 'bigdata-team',
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

def check_cluster_health(**context):
    """Verifica saúde do cluster EMR."""
    print("Verificando saúde dos clusters EMR...")

    # Conectar ao EMR (simplificado)
    # aws_hook = AwsBaseHook(aws_conn_id='aws_default')
    # emr_client = aws_hook.get_client_type('emr')

    # Simulação de health check
    metrics = {
        'active_clusters': 2,
        'cpu_usage': 65,
        'memory_usage': 72,
        'status': 'healthy'
    }

    print(f"Status do cluster: {metrics['status']}")
    print(f"CPU Usage: {metrics['cpu_usage']}%")
    print(f"Memory Usage: {metrics['memory_usage']}%")

    return metrics

def check_cost_budget(**context):
    """Monitora custos e compara com orçamento."""
    print("Verificando custos AWS...")

    # Simulação de verificação de custos
    daily_cost = 45.30
    monthly_budget = 2000.00
    current_month_cost = 890.50

    budget_percentage = (current_month_cost / monthly_budget) * 100

    print(f"Custo diário: ${daily_cost}")
    print(f"Custo mensal acumulado: ${current_month_cost}")
    print(f"Orçamento utilizado: {budget_percentage:.1f}%")

    if budget_percentage > 80:
        print("⚠️  ALERTA: Orçamento acima de 80%!")

    return {
        'daily_cost': daily_cost,
        'monthly_cost': current_month_cost,
        'budget_percentage': budget_percentage
    }

def check_data_quality(**context):
    """Verifica qualidade dos dados processados."""
    print("Verificando qualidade dos dados...")

    # Simulação de verificação de qualidade
    metrics = {
        'total_records': 1500000,
        'null_values': 250,
        'duplicates': 120,
        'error_rate': 0.025
    }

    print(f"Total de registros: {metrics['total_records']}")
    print(f"Taxa de erro: {metrics['error_rate']:.3f}%")

    if metrics['error_rate'] > 0.05:
        print("⚠️  ALERTA: Taxa de erro acima do limite!")

    return metrics

def send_daily_report(**context):
    """Consolida métricas e envia relatório."""
    ti = context['task_instance']

    # Recupera resultados das tasks anteriores
    health = ti.xcom_pull(task_ids='check_cluster_health')
    costs = ti.xcom_pull(task_ids='check_cost_budget')
    quality = ti.xcom_pull(task_ids='check_data_quality')

    print("\n" + "="*50)
    print("RELATÓRIO DIÁRIO DE MONITORAMENTO")
    print("="*50)
    print(f"\n1. SAÚDE DO CLUSTER:")
    print(f"   - Status: {health.get('status', 'N/A')}")
    print(f"   - CPU: {health.get('cpu_usage', 0)}%")
    print(f"\n2. CUSTOS:")
    print(f"   - Diário: ${costs.get('daily_cost', 0)}")
    print(f"   - Orçamento: {costs.get('budget_percentage', 0):.1f}%")
    print(f"\n3. QUALIDADE:")
    print(f"   - Registros: {quality.get('total_records', 0)}")
    print(f"   - Erro: {quality.get('error_rate', 0):.3f}%")
    print("="*50 + "\n")

with DAG(
    'cluster_monitoring',
    default_args=default_args,
    description='Monitoramento contínuo de clusters e custos',
    schedule_interval='0 */6 * * *',  # A cada 6 horas
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['monitoring', 'alerts', 'costs'],
) as dag:

    health_check = PythonOperator(
        task_id='check_cluster_health',
        python_callable=check_cluster_health,
    )

    cost_check = PythonOperator(
        task_id='check_cost_budget',
        python_callable=check_cost_budget,
    )

    quality_check = PythonOperator(
        task_id='check_data_quality',
        python_callable=check_data_quality,
    )

    report = PythonOperator(
        task_id='send_daily_report',
        python_callable=send_daily_report,
    )

    # Executar checks em paralelo, depois gerar relatório
    [health_check, cost_check, quality_check] >> report
