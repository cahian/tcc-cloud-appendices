/**
 * Configuração de Buckets S3
 */

resource "aws_s3_bucket" "data_lake" {
  bucket = var.data_lake_bucket_name

  tags = {
    Name        = "TCC Big Data Lake"
    Environment = "production"
    Project     = var.project_name
  }
}

resource "aws_s3_bucket" "logs" {
  bucket = var.logs_bucket_name

  tags = {
    Name        = "TCC EMR Logs"
    Environment = "production"
    Project     = var.project_name
  }
}

resource "aws_s3_bucket_lifecycle_configuration" "data_lake_lifecycle" {
  bucket = aws_s3_bucket.data_lake.id

  rule {
    id     = "archive-old-data"
    status = "Enabled"

    transition {
      days          = 90
      storage_class = "GLACIER"
    }

    expiration {
      days = 365
    }
  }
}
