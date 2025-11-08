# Apêndice E - Dados Experimentais e Configurações dos Clusters

Conjunto de arquivos que documentam os experimentos realizados, resultados consolidados e as configurações finais recomendadas dos clusters utilizados no TCC.

## Arquivos

- `experiment_results.csv` — resultados completos (framework, dataset, nós, tempo, custo, throughput).
- `cluster_configs.yaml` — parâmetros de hardware e ajustes Spark/Hadoop utilizados nas execuções finais.
- `analyze_results.py` — script utilitário para gerar estatísticas e comparar frameworks a partir do CSV.

## Como utilizar

### 1. Instalar dependências
Nenhuma dependência externa é necessária; o script utiliza apenas bibliotecas padrão do Python 3.9+.

### 2. Gerar relatório resumido

```bash
cd appendices/E_experiments
python3 analyze_results.py
```

Saída esperada:
- Melhor framework por dataset
- Média/mediana de tempo e custo
- Throughput agregado

### 3. Replicar configurações
Abra `cluster_configs.yaml` para visualizar as combinações de tipos de instância, ajustes Spark e políticas de auto-scaling. O arquivo está organizado por cenário:
- `balanced_100gb`
- `high_throughput_1tb`
- `cost_optimized_spot`

## Estrutura do CSV

| Coluna           | Descrição                                 |
|------------------|-------------------------------------------|
| `framework`      | spark, hadoop ou bigquery                 |
| `dataset_gb`     | Volume processado em GB                   |
| `nodes`          | Número de nós (N/A para BigQuery)         |
| `time_min`       | Tempo médio em minutos                    |
| `cost_usd`       | Custo estimado em dólar                   |
| `throughput_gbps`| Throughput médio em GB/s                  |

## Observações
- Os valores refletem a média de 10 execuções realizadas entre dezembro/2024 e janeiro/2025.
- BigQuery aparece com `nodes=0` por se tratar de serviço serverless.
- Todos os scripts podem ser executados em modo offline, sem necessidade de credenciais AWS.
