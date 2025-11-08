output "cluster_id" {
  description = "ID do cluster EMR"
  value       = aws_emr_cluster.bigdata_cluster.id
}

output "cluster_name" {
  description = "Nome do cluster EMR"
  value       = aws_emr_cluster.bigdata_cluster.name
}

output "master_public_dns" {
  description = "DNS público do nó master"
  value       = aws_emr_cluster.bigdata_cluster.master_public_dns
}

output "data_lake_bucket" {
  description = "Bucket S3 do Data Lake"
  value       = aws_s3_bucket.data_lake.bucket
}

output "logs_bucket" {
  description = "Bucket S3 de logs"
  value       = aws_s3_bucket.logs.bucket
}
