terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# DynamoDB table for storing conversations (Gesprachen)
resource "aws_dynamodb_table" "alle_gesprache" {
  name           = var.table_name
  billing_mode   = var.billing_mode
  hash_key       = "gesprach_name"

  attribute {
    name = "gesprach_name"
    type = "S"
  }

  # Enable point-in-time recovery for data protection
  point_in_time_recovery {
    enabled = var.enable_point_in_time_recovery
  }

  # Enable server-side encryption
  server_side_encryption {
    enabled = true
  }

  # Tags for resource management
  tags = merge(
    var.common_tags,
    {
      Name        = var.table_name
      Environment = var.env
      Project     = "sprachweg"
    }
  )
}

