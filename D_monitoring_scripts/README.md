# Apêndice D - Scripts de Monitoramento e Coleta de Métricas

Scripts para monitoramento de performance, custos e eficiência energética.

## Scripts Disponíveis

### 1. **cloudwatch_metrics.py** - Coletor CloudWatch
Publica e recupera métricas do AWS CloudWatch.

**Funcionalidades:**
- Publicação de métricas customizadas
- Monitoramento de performance de jobs
- Integração com EMR clusters

**Uso:**
```python
from cloudwatch_metrics import CloudWatchMetricsCollector

collector = CloudWatchMetricsCollector()
collector.monitor_performance(job_id='spark-123', duration_seconds=1850)
```

### 2. **benchmark_suite.py** - Suite de Benchmarks
Executa testes de performance e escalabilidade.

**Funcionalidades:**
- Testes de throughput
- Testes de escalabilidade (2-16 nodes)
- Comparação entre tecnologias (Hadoop, Spark, BigQuery)
- Estatísticas detalhadas

**Uso:**
```bash
python benchmark_suite.py
```

**Saída:**
- Throughput (GB/hora e MB/segundo)
- Estatísticas (média, mediana, desvio padrão)
- Comparação de speedup entre tecnologias

### 3. **cost_tracker.py** - Rastreador de Custos
Calcula e compara custos de infraestrutura AWS.

**Funcionalidades:**
- Cálculo de custo por job
- Comparação Spot vs On-Demand
- Estimativa de custo mensal
- Custo por GB processado

**Uso:**
```python
from cost_tracker import CostTracker

tracker = CostTracker()
cost = tracker.calculate_job_cost(
    master_type='m5.xlarge',
    worker_type='c5.2xlarge',
    worker_count=4,
    duration_hours=1.5,
    data_processed_gb=100,
    use_spot=True
)
```

**Preços incluídos:**
- EC2 instances (on-demand e spot)
- EMR fees (25% adicional)
- S3 storage
- Data transfer

### 4. **energy_monitor.py** - Monitor de Eficiência Energética
Calcula consumo de energia e pegada de carbono.

**Funcionalidades:**
- Cálculo de consumo energético (kWh)
- Pegada de carbono (kg CO₂)
- Eficiência por TB processado
- Comparação entre regiões AWS

**Uso:**
```python
from energy_monitor import EnergyMonitor

monitor = EnergyMonitor(region='us-east-1')
monitor.job_energy_report(
    master_type='m5.xlarge',
    worker_type='c5.2xlarge',
    worker_count=4,
    duration_hours=1.5,
    data_processed_gb=250
)

### 5. **monitor_job.py** - Acompanhamento de clusters EMR
Supervisiona clusters EMR em tempo real usando `describe_cluster` e métricas do CloudWatch. Inclui modo `--dry-run` para execução local sem credenciais.

**Uso:**
```bash
python monitor_job.py --cluster-id j-XXXXXXXX --dry-run
```

**Parâmetros-chave:**
- `--interval`: intervalo entre leituras (segundos, padrão 30)
- `--timeout`: tempo máximo de monitoramento em minutos (padrão 60)
- `--region`: região AWS (padrão us-east-1)
- `--dry-run`: habilita respostas simuladas para testes locais
```

**Métricas:**
- kWh/TB processado
- kg CO₂/TB processado
- PUE (Power Usage Effectiveness): 1.15
- Fatores de emissão por região

## Instalação

```bash
pip install -r requirements.txt
```

## Configuração AWS

Para usar os scripts que interagem com AWS, configure suas credenciais:

```bash
aws configure
```

Ou via variáveis de ambiente:
```bash
export AWS_ACCESS_KEY_ID=your_key
export AWS_SECRET_ACCESS_KEY=your_secret
export AWS_DEFAULT_REGION=us-east-1
```

## Exemplos de Uso

### Monitoramento Completo de um Job

```python
from cloudwatch_metrics import CloudWatchMetricsCollector
from cost_tracker import CostTracker
from energy_monitor import EnergyMonitor

# Configuração do job
job_config = {
    'master_type': 'm5.xlarge',
    'worker_type': 'c5.2xlarge',
    'worker_count': 4,
    'duration_hours': 1.5,
    'data_gb': 250
}

# Métricas de performance
collector = CloudWatchMetricsCollector()
collector.monitor_performance('job-123', int(job_config['duration_hours'] * 3600))

# Análise de custos
tracker = CostTracker()
cost = tracker.calculate_job_cost(**job_config, use_spot=True)
print(f"Custo total: ${cost['total_cost']:.2f}")

# Análise energética
monitor = EnergyMonitor()
efficiency = monitor.job_energy_report(**job_config)
print(f"Eficiência: {efficiency['kwh_per_tb']:.2f} kWh/TB")
```

## Métricas Baseadas no TCC

Os scripts implementam as métricas documentadas no TCC:

- **Performance**: Throughput de até 2.5 TB/hora (cluster 16 nodes)
- **Speedup**: Spark 1.53x, BigQuery 2.08x vs Hadoop
- **Custos**: Economia de 42% com spot instances
- **Energia**: Eficiência variável por região (0.098-0.385 kg CO₂/kWh)
