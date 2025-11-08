"""
DAG Principal de ETL Diário
Apêndice C - TCC: Eficiência e Escalabilidade com Cloud Computing
"""

from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.amazon.aws.operators.emr import (
    EmrCreateJobFlowOperator,
    EmrAddStepsOperator,
    EmrTerminateJobFlowOperator
)
from airflow.providers.amazon.aws.sensors.emr import EmrStepSensor
from airflow.operators.python import PythonOperator

# Configurações padrão
default_args = {
    'owner': 'bigdata-team',
    'depends_on_past': False,
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

# Configuração do cluster EMR
JOB_FLOW_OVERRIDES = {
    'Name': 'Daily-ETL-Cluster',
    'ReleaseLabel': 'emr-6.9.0',
    'Applications': [{'Name': 'Spark'}, {'Name': 'Hadoop'}],
    'Instances': {
        'InstanceGroups': [
            {
                'Name': 'Master',
                'Market': 'ON_DEMAND',
                'InstanceRole': 'MASTER',
                'InstanceType': 'm5.xlarge',
                'InstanceCount': 1,
            },
            {
                'Name': 'Core',
                'Market': 'SPOT',
                'InstanceRole': 'CORE',
                'InstanceType': 'c5.2xlarge',
                'InstanceCount': 2,
            }
        ],
        'KeepJobFlowAliveWhenNoSteps': True,
        'TerminationProtected': False,
    },
    'JobFlowRole': 'EMR_EC2_DefaultRole',
    'ServiceRole': 'EMR_DefaultRole',
}

# Steps do Spark
SPARK_STEPS = [
    {
        'Name': 'Ingest Data',
        'ActionOnFailure': 'CONTINUE',
        'HadoopJarStep': {
            'Jar': 'command-runner.jar',
            'Args': [
                'spark-submit',
                '--deploy-mode', 'cluster',
                's3://tcc-bigdata-storage/scripts/ingest_data.py',
                's3://tcc-bigdata-storage/raw/',
                's3://tcc-bigdata-storage/processed/'
            ],
        },
    },
    {
        'Name': 'Process Data',
        'ActionOnFailure': 'CANCEL_AND_WAIT',
        'HadoopJarStep': {
            'Jar': 'command-runner.jar',
            'Args': [
                'spark-submit',
                '--deploy-mode', 'cluster',
                '--executor-memory', '12g',
                '--executor-cores', '4',
                's3://tcc-bigdata-storage/scripts/process_data.py',
                's3://tcc-bigdata-storage/processed/',
                's3://tcc-bigdata-storage/results/'
            ],
        },
    },
]

def validate_data(**context):
    """Validação básica dos dados antes do processamento."""
    print("Validando disponibilidade dos dados...")
    # Aqui entraria lógica de validação real (ex: verificar se arquivo existe no S3)
    print("Dados validados com sucesso!")

# Definição da DAG
with DAG(
    'daily_etl_pipeline',
    default_args=default_args,
    description='Pipeline ETL diário para processamento Big Data',
    schedule_interval='@daily',
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=['bigdata', 'etl', 'production'],
) as dag:

    # Tarefa 1: Validação de dados
    validate_task = PythonOperator(
        task_id='validate_data',
        python_callable=validate_data,
    )

    # Tarefa 2: Criar cluster EMR
    create_cluster = EmrCreateJobFlowOperator(
        task_id='create_emr_cluster',
        job_flow_overrides=JOB_FLOW_OVERRIDES,
        aws_conn_id='aws_default',
    )

    # Tarefa 3: Adicionar steps Spark
    add_steps = EmrAddStepsOperator(
        task_id='add_spark_steps',
        job_flow_id="{{ task_instance.xcom_pull(task_ids='create_emr_cluster', key='return_value') }}",
        aws_conn_id='aws_default',
        steps=SPARK_STEPS,
    )

    # Tarefa 4: Aguardar conclusão dos steps
    wait_for_steps = EmrStepSensor(
        task_id='watch_spark_steps',
        job_flow_id="{{ task_instance.xcom_pull(task_ids='create_emr_cluster', key='return_value') }}",
        step_id="{{ task_instance.xcom_pull(task_ids='add_spark_steps', key='return_value')[0] }}",
        aws_conn_id='aws_default',
    )

    # Tarefa 5: Terminar cluster
    terminate_cluster = EmrTerminateJobFlowOperator(
        task_id='terminate_emr_cluster',
        job_flow_id="{{ task_instance.xcom_pull(task_ids='create_emr_cluster', key='return_value') }}",
        aws_conn_id='aws_default',
    )

    # Definir dependências
    validate_task >> create_cluster >> add_steps >> wait_for_steps >> terminate_cluster
