/**
 * Configuração do Cluster EMR com Auto-scaling
 */

resource "aws_emr_cluster" "bigdata_cluster" {
  name          = "${var.project_name}-cluster"
  release_label = var.emr_release
  applications  = ["Spark", "Hadoop"]

  service_role     = aws_iam_role.emr_service_role.arn
  autoscaling_role = aws_iam_role.emr_autoscaling_role.arn
  log_uri          = "s3://${aws_s3_bucket.logs.bucket}/logs/"

  ec2_attributes {
    instance_profile = aws_iam_instance_profile.emr_ec2_profile.arn
    subnet_id        = aws_subnet.main.id
  }

  # Nó Master
  master_instance_group {
    instance_type  = var.master_instance_type
    instance_count = 1
  }

  # Nós Core com Auto-scaling
  core_instance_group {
    instance_type  = var.core_instance_type
    instance_count = var.core_instance_count

    ebs_config {
      size                 = 100
      type                 = "gp3"
      volumes_per_instance = 1
    }

    autoscaling_policy = jsonencode({
      Constraints = {
        MinCapacity = var.core_instance_count
        MaxCapacity = var.max_core_instances
      }
      Rules = [
        {
          Name        = "Scale-up-on-YARNMemory"
          Description = "Scale up when YARN memory is above 70%"
          Action = {
            SimpleScalingPolicyConfiguration = {
              AdjustmentType    = "CHANGE_IN_CAPACITY"
              ScalingAdjustment = 2
              CoolDown          = 300
            }
          }
          Trigger = {
            CloudWatchAlarmDefinition = {
              ComparisonOperator = "GREATER_THAN"
              EvaluationPeriods  = 1
              MetricName         = "YARNMemoryAvailablePercentage"
              Namespace          = "AWS/ElasticMapReduce"
              Period             = 300
              Statistic          = "AVERAGE"
              Threshold          = 70.0
            }
          }
        },
        {
          Name        = "Scale-down-on-YARNMemory"
          Description = "Scale down when YARN memory is below 30%"
          Action = {
            SimpleScalingPolicyConfiguration = {
              AdjustmentType    = "CHANGE_IN_CAPACITY"
              ScalingAdjustment = -1
              CoolDown          = 300
            }
          }
          Trigger = {
            CloudWatchAlarmDefinition = {
              ComparisonOperator = "LESS_THAN"
              EvaluationPeriods  = 1
              MetricName         = "YARNMemoryAvailablePercentage"
              Namespace          = "AWS/ElasticMapReduce"
              Period             = 300
              Statistic          = "AVERAGE"
              Threshold          = 30.0
            }
          }
        }
      ]
    })
  }

  # Configurações Spark otimizadas
  configurations_json = jsonencode([
    {
      Classification = "spark-defaults"
      Properties = {
        "spark.executor.memory"                         = "12g"
        "spark.executor.cores"                          = "4"
        "spark.sql.adaptive.enabled"                    = "true"
        "spark.dynamicAllocation.enabled"               = "true"
        "spark.sql.adaptive.coalescePartitions.enabled" = "true"
      }
    }
  ])

  tags = {
    Name        = "BigData EMR Cluster"
    Environment = "production"
  }
}
