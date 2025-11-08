/**
 * Apêndice B - Configurações Terraform para Infraestrutura AWS
 * TCC: Eficiência e Escalabilidade com Cloud Computing
 */

terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}
