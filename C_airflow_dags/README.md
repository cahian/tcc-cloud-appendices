# Apêndice C - DAGs do Apache Airflow para Orquestração

DAGs (Directed Acyclic Graphs) para orquestração automatizada de pipelines Big Data.

## DAGs Disponíveis

### 1. **daily_etl_dag.py** - Pipeline ETL Principal
- **Schedule**: Diário (@daily)
- **Função**: Orquestra o processamento completo de dados
- **Fluxo**:
  1. Validação de dados
  2. Criação do cluster EMR
  3. Submissão de jobs Spark (ingest + process)
  4. Monitoramento de execução
  5. Encerramento do cluster

### 2. **scalability_test_dag.py** - Testes de Escalabilidade
- **Schedule**: Semanal (@weekly)
- **Função**: Executa benchmarks automatizados
- **Datasets**: 100GB, 500GB, 1TB
- **Métricas**: Tempo de execução, throughput
- **Observação**: As tasks utilizam `PythonOperator` com simulação (`time.sleep`) para permitir execução local sem recursos AWS. Substitua por operadores EMR reais conforme necessidade.

### 3. **monitoring_dag.py** - Monitoramento Contínuo
- **Schedule**: A cada 6 horas
- **Função**: Monitora saúde, custos e qualidade
- **Alertas**: Budget > 80%, Error rate > 5%
- **Observação**: Métricas são mockadas para documentação. Integre com `AwsBaseHook`/CloudWatch para uso em produção.

## Instalação

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Configurar Airflow

```bash
# Inicializar banco de dados
airflow db init

# Criar usuário admin
airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com
```

### 3. Copiar DAGs

```bash
cp dags/*.py $AIRFLOW_HOME/dags/
```

### 4. Configurar Conexão AWS

No Airflow UI, adicione uma conexão:
- **Conn Id**: `aws_default`
- **Conn Type**: `Amazon Web Services`
- **Extra**: `{"region_name": "us-east-1"}`

## Uso

### Iniciar Airflow

```bash
# Terminal 1: Webserver
airflow webserver --port 8080

# Terminal 2: Scheduler
airflow scheduler
```

### Acessar UI

Abra `http://localhost:8080` no navegador.

### Executar DAG Manualmente

```bash
airflow dags trigger daily_etl_pipeline
```

## Estrutura de Dependências

### daily_etl_pipeline
```
validate_data → create_cluster → add_steps → watch_steps → terminate_cluster
```

### scalability_testing
```
[benchmark_100gb, benchmark_500gb, benchmark_1tb] → aggregate_results
```

### cluster_monitoring
```
[health_check, cost_check, quality_check] → send_report
```

## Configurações Importantes

- **Retries**: 2 tentativas com delay de 5 minutos
- **Email Alerts**: Habilitado para falhas
- **Cluster Type**: Spot instances para workers
- **Auto-termination**: Cluster encerra após jobs
