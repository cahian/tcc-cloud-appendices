variable "aws_region" {
  description = "Região AWS para deploy"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Nome do projeto"
  type        = string
  default     = "tcc-bigdata"
}

variable "master_instance_type" {
  description = "Tipo de instância para nó master"
  type        = string
  default     = "m5.xlarge"
}

variable "core_instance_type" {
  description = "Tipo de instância para nós workers"
  type        = string
  default     = "c5.2xlarge"
}

variable "core_instance_count" {
  description = "Número de instâncias core"
  type        = number
  default     = 2
}

variable "max_core_instances" {
  description = "Máximo de instâncias com auto-scaling"
  type        = number
  default     = 16
}

variable "emr_release" {
  description = "Versão do EMR"
  type        = string
  default     = "emr-6.9.0"
}

variable "data_lake_bucket_name" {
  description = "Nome do bucket S3 principal (ex: tcc-bigdata-storage)"
  type        = string
  default     = "tcc-bigdata-storage"
}

variable "logs_bucket_name" {
  description = "Nome do bucket S3 para logs (ex: tcc-bigdata-logs)"
  type        = string
  default     = "tcc-bigdata-logs"
}
