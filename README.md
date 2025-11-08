# Apêndices do TCC - Eficiência e Escalabilidade com Cloud Computing

Scripts completos do protótipo desenvolvido para processamento Big Data em nuvem AWS.

**Autor:** Cahian Freire
**Instituição:** Universidade Paulista (UNIP)
**Ano:** 2025

---

## 📋 Índice de Apêndices

### [Apêndice A - Scripts Python/PySpark](A_spark_scripts/)
Scripts de processamento distribuído de dados com Apache Spark 3.2.0.

**Arquivos:**
- [`ingest_data.py`](A_spark_scripts/ingest_data.py) - Ingestão de dados do S3 com validação
- [`process_data.py`](A_spark_scripts/process_data.py) - Processamento ETL e agregações
- [`spark_optimizer.py`](A_spark_scripts/spark_optimizer.py) - Configurações otimizadas

**Tecnologias:** PySpark 3.2.0, boto3, PyArrow

---

### [Apêndice B - Configurações Terraform](B_terraform/)
Infraestrutura como Código para provisionamento AWS.

**Arquivos:**
- [`main.tf`](B_terraform/main.tf) - Provider AWS
- [`emr_cluster.tf`](B_terraform/emr_cluster.tf) - Cluster EMR com auto-scaling
- [`s3.tf`](B_terraform/s3.tf) - Buckets S3 (Data Lake + Logs)
- [`iam.tf`](B_terraform/iam.tf) - Roles e policies
- [`network.tf`](B_terraform/network.tf) - VPC e subnets
- [`variables.tf`](B_terraform/variables.tf) - Variáveis configuráveis
- [`outputs.tf`](B_terraform/outputs.tf) - Outputs do cluster

**Recursos:** EMR cluster, S3, VPC, IAM, Auto-scaling (2-16 nodes)

---

### [Apêndice C - DAGs Apache Airflow](C_airflow_dags/)
Orquestração automatizada de pipelines Big Data.

**DAGs:**
- [`daily_etl_dag.py`](C_airflow_dags/dags/daily_etl_dag.py) - Pipeline ETL diário
- [`scalability_test_dag.py`](C_airflow_dags/dags/scalability_test_dag.py) - Testes de escalabilidade
- [`monitoring_dag.py`](C_airflow_dags/dags/monitoring_dag.py) - Monitoramento contínuo

**Schedule:**
- ETL: Diário (@daily)
- Benchmarks: Semanal (@weekly)
- Monitoring: A cada 6 horas

---

### [Apêndice D - Scripts de Monitoramento](D_monitoring_scripts/)
Coleta de métricas, análise de custos e eficiência energética.

**Scripts:**
- [`cloudwatch_metrics.py`](D_monitoring_scripts/cloudwatch_metrics.py) - Métricas AWS CloudWatch
- [`benchmark_suite.py`](D_monitoring_scripts/benchmark_suite.py) - Suite de benchmarks
- [`cost_tracker.py`](D_monitoring_scripts/cost_tracker.py) - Análise de custos
- [`energy_monitor.py`](D_monitoring_scripts/energy_monitor.py) - Eficiência energética
- [`monitor_job.py`](D_monitoring_scripts/monitor_job.py) - Monitoramento contínuo de clusters EMR (suporte a `--dry-run`)

**Funcionalidades:**
- Performance: Throughput, latência, escalabilidade
- Custos: Spot vs On-Demand, custo/GB, estimativas mensais
- Energia: kWh/TB, pegada de carbono, comparação regional
- Monitoramento: status dos clusters, métricas CloudWatch, alertas básicos

---

### [Apêndice E - Dados Experimentais e Configurações](E_experiments/)
Resultados completos dos experimentos e configurações recomendadas.

**Arquivos:**
- [`experiment_results.csv`](E_experiments/experiment_results.csv) - Tabelas completas das execuções
- [`cluster_configs.yaml`](E_experiments/cluster_configs.yaml) - Ajustes finais de hardware/Spark
- [`analyze_results.py`](E_experiments/analyze_results.py) - Script para gerar estatísticas
- [`README.md`](E_experiments/README.md) - Guia de uso

---

## 🚀 Quick Start

### Requisitos

```bash
# Python 3.9+
pip install -r A_spark_scripts/requirements.txt
pip install -r C_airflow_dags/requirements.txt
pip install -r D_monitoring_scripts/requirements.txt

# Terraform 1.0+ (para Apêndice B)
# AWS CLI configurado
```

### Testes Rápidos

```bash
# Testar otimizador Spark
python3 A_spark_scripts/spark_optimizer.py

# Executar benchmarks
python3 D_monitoring_scripts/benchmark_suite.py

# Análise de custos
python3 D_monitoring_scripts/cost_tracker.py

# Análise energética
python3 D_monitoring_scripts/energy_monitor.py

# Monitoramento (modo simulado)
python3 D_monitoring_scripts/monitor_job.py --cluster-id demo --dry-run

# Estatísticas dos experimentos
python3 E_experiments/analyze_results.py
```

### Validação Terraform

```bash
cd B_terraform
terraform init
terraform validate
terraform plan
```

---

## 📊 Resultados Principais (do TCC)

### Performance
- **Apache Spark:** 35% mais rápido que Hadoop (speedup 1.53x)
- **Google BigQuery:** 108% mais rápido que Hadoop (speedup 2.08x)
- **Throughput máximo:** 2.5 TB/hora (cluster 16 nodes)

### Custos
- **Economia com Spot:** 60% vs On-Demand
- **Redução total:** 42% com auto-scaling + spot
- **Custo médio:** $0.10/GB processado

### Escalabilidade
- **Auto-scaling:** 2-16 instâncias
- **Eficiência:** ~80% linear até 16 nodes
- **Threshold:** Scale-up em 70% CPU, Scale-down em 30%

### Sustentabilidade
- **Melhor região:** sa-east-1 (0.098 kg CO₂/kWh - hidrelétrica)
- **Pior região:** us-east-1 (0.385 kg CO₂/kWh)
- **Redução potencial:** 74.5% mudando de região

---

## 📁 Estrutura Completa

```
appendices/
├── A_spark_scripts/
│   ├── ingest_data.py (91 linhas)
│   ├── process_data.py (81 linhas)
│   ├── spark_optimizer.py (76 linhas)
│   ├── requirements.txt
│   └── README.md
├── B_terraform/
│   ├── main.tf
│   ├── variables.tf (46 linhas)
│   ├── s3.tf (48 linhas)
│   ├── iam.tf (92 linhas)
│   ├── emr_cluster.tf (124 linhas)
│   ├── network.tf (54 linhas)
│   ├── outputs.tf (27 linhas)
│   └── README.md
├── C_airflow_dags/
│   ├── dags/
│   │   ├── daily_etl_dag.py (142 linhas)
│   │   ├── scalability_test_dag.py (90 linhas)
│   │   └── monitoring_dag.py (143 linhas)
│   ├── requirements.txt
│   └── README.md
├── D_monitoring_scripts/
│   ├── cloudwatch_metrics.py (115 linhas)
│   ├── benchmark_suite.py (143 linhas)
│   ├── cost_tracker.py (243 linhas)
│   ├── energy_monitor.py (257 linhas)
│   ├── monitor_job.py (170 linhas)
│   ├── requirements.txt
│   └── README.md
├── E_experiments/
│   ├── experiment_results.csv (10 linhas)
│   ├── cluster_configs.yaml (36 linhas)
│   ├── analyze_results.py (90 linhas)
│   └── README.md
└── README.md (este arquivo)

Total: ~1.9k linhas de código/dados
```

---

## ✅ Validações Realizadas

- ✅ **Sintaxe Python:** Todos os scripts compilam sem erros
- ✅ **Testes funcionais:** Benchmark, custos e energia executados com sucesso
- ✅ **Terraform:** Sintaxe validada (fmt + validate)
- ✅ **Airflow DAGs:** Sintaxe validada
- ✅ **Documentação:** READMEs completos em cada apêndice

---

## 📖 Como Usar no TCC

Cada apêndice foi projetado para ser auto-contido e pode ser referenciado diretamente:

**Exemplo de citação:**
> "O código completo do processamento Spark está disponível no Apêndice A,
> incluindo otimizações de configuração conforme descrito no arquivo
> `spark_optimizer.py` (linhas 15-35)."

---

## 🔗 Referências Técnicas

- **Apache Spark:** 3.2.0
- **Hadoop:** 3.3.1
- **EMR Release:** emr-6.9.0
- **Terraform:** >= 1.0
- **Airflow:** 2.7.0
- **Python:** 3.9+
- **AWS Provider:** ~> 4.0

---

## 📝 Licença

Este código foi desenvolvido para fins acadêmicos como parte do TCC de
Bacharelado em Ciência da Computação da UNIP (2025).

---

**Data de criação:** Novembro 2025
**Última atualização:** {{ data_atual }}
