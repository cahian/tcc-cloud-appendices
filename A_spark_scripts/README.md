# Apêndice A - Scripts Python para Processamento Spark

Scripts de processamento distribuído de Big Data utilizando Apache Spark 3.2.0.

## Arquivos

- **ingest_data.py**: Ingestão de dados do S3 com validação de schema
- **process_data.py**: Processamento ETL com agregações e transformações
- **spark_optimizer.py**: Utilitários de otimização para diferentes workloads

## Requisitos

```bash
pip install -r requirements.txt
```

## Uso

### 1. Ingestão de Dados

```bash
spark-submit ingest_data.py s3://bucket/input/ s3://bucket/output/
```

### 2. Processamento ETL

```bash
spark-submit --executor-memory 12g \
             --executor-cores 4 \
             process_data.py s3://bucket/output/ s3://bucket/results/
```

### 3. Otimizador Spark

```python
from spark_optimizer import SparkOptimizer

# Criar sessão otimizada
spark = SparkOptimizer.get_optimized_session("balanced")
```

## Configurações de Performance

- **Adaptive Execution**: Habilitado para otimização dinâmica
- **Dynamic Allocation**: Ajusta recursos automaticamente
- **Executor Memory**: 12GB por executor
- **Executor Cores**: 4 cores por executor

## Dataset Suportado

- NYC Taxi Dataset (formato CSV/Parquet)
- Schema com 9 campos principais (vendor_id, timestamps, distância, valores)
