terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
    archive = {
      source  = "hashicorp/archive"
      version = "~> 2.4"
    }
  }
}

# DynamoDB table for storing conversations (Gesprachen)
resource "aws_dynamodb_table" "alle_gesprache" {
  name           = var.TABLE_NAME
  billing_mode   = var.BILLING_MODE
  hash_key       = "k"
  range_key      = "sk"

  attribute {
    name = "k"
    type = "S"
  }

  attribute {
    name = "sk"
    type = "S"
  }

  # Enable point-in-time recovery for data protection
  point_in_time_recovery {
    enabled = var.ENABLE_POINT_IN_TIME_RECOVERY
  }

  # Enable server-side encryption
  server_side_encryption {
    enabled = true
  }

  # Tags for resource management
  tags = merge(
    var.COMMON_TAGS,
    {
      Name        = var.TABLE_NAME
      Environment = var.ENV
      Project     = "sprachweg"
    }
  )
}

