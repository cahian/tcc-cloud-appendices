# Apêndice B - Configurações Terraform para Infraestrutura AWS

Infraestrutura como Código (IaC) para provisionamento de cluster EMR com auto-scaling.

## Recursos Provisionados

- **EMR Cluster**: Spark 3.2.0 + Hadoop 3.3.1
- **Auto-scaling**: 2-16 instâncias (baseado em uso de YARN)
- **S3 Buckets**: Data Lake + Logs
- **VPC**: Rede isolada
- **IAM Roles**: Service role, EC2 profile, Auto-scaling role

## Estrutura de Arquivos

- `main.tf`: Provider AWS
- `variables.tf`: Variáveis configuráveis
- `emr_cluster.tf`: Configuração do cluster EMR
- `s3.tf`: Buckets S3
- `iam.tf`: Roles e policies
- `network.tf`: VPC e subnets
- `outputs.tf`: Outputs úteis

## Uso

### 1. Inicializar Terraform

```bash
terraform init
```

### 2. Validar Configuração

```bash
terraform validate
terraform plan
```

### 3. Provisionar Infraestrutura

```bash
terraform apply
```

### 4. Destruir Recursos (quando não precisar mais)

```bash
terraform destroy
```

## Customização

Edite `variables.tf` para ajustar:
- Região AWS (`aws_region`)
- Tipo de instâncias (`master_instance_type`, `core_instance_type`)
- Número de workers (`core_instance_count`, `max_core_instances`)
- Nomes dos buckets S3 (`data_lake_bucket_name`, `logs_bucket_name`) — por padrão `tcc-bigdata-storage` e `tcc-bigdata-logs`

## Configurações de Auto-scaling

- **Scale-up**: Quando YARN memory > 70%
- **Scale-down**: Quando YARN memory < 30%
- **Cooldown**: 5 minutos entre ajustes

## Custos Estimados

- Master (m5.xlarge): ~$0.192/hora
- Workers (c5.2xlarge): ~$0.34/hora cada
- Cluster mínimo (2 workers): ~$0.87/hora
