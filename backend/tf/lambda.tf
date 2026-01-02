# Shared IAM role for all Lambda functions
resource "aws_iam_role" "lambda_execution_role" {
  name = "${var.ENV}-sprachweg-lambda-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })

  tags = merge(
    var.COMMON_TAGS,
    {
      Name        = "${var.ENV}-sprachweg-lambda-role"
      ENVironment = var.ENV
      Project     = "sprachweg"
    }
  )
}

# IAM policy attachment for basic Lambda execution
resource "aws_iam_role_policy_attachment" "lambda_basic_execution" {
  role       = aws_iam_role.lambda_execution_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

# IAM policy for DynamoDB access
resource "aws_iam_role_policy" "lambda_dynamodb_access" {
  name = "${var.ENV}-lambda-dynamodb-access"
  role = aws_iam_role.lambda_execution_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem",
          "dynamodb:Query",
          "dynamodb:Scan"
        ]
        Resource = [
          aws_dynamodb_table.alle_gesprache.arn,
          "${aws_dynamodb_table.alle_gesprache.arn}/*"
        ]
      }
    ]
  })
}

# Archive the entire python directory (handlers + sprachweg module)
data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../python"
  output_path = "${path.module}/apps/app1/lambda_package.zip"
  excludes = [
    "__pycache__",
    "*.pyc",
    "*.pyo",
    "*.pyd",
    ".pytest_cache",
    "*.egg-info"
  ]
}

# Define handlers - easy to add more handlers here
locals {
  handlers = {
    test_handler = {
      handler_function = "handlers.test_handler.hello_world"
      description      = "Test handler for hello world"
    }
    # gesprache_handler = {
    #   handler_function = "handlers.gesprache_handler.alle_gesprache_erhalten_handler"
    #   description      = "Handler for managing conversations (Gesprachen)"
    # }
    # ki_handler = {
    #   handler_function = "handlers.ki_handler.nachricht_senden_handler"
    #   description      = "Handler for AI message sending"
    # }
  }
}

# Create Lambda function for each handler
resource "aws_lambda_function" "handler" {
  for_each = local.handlers

  filename         = data.archive_file.lambda_zip.output_path
  function_name    = "${var.ENV}-${each.key}"
  role            = aws_iam_role.lambda_execution_role.arn
  handler         = each.value.handler_function
  runtime         = "python3.12"
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  description     = each.value.description
  timeout         = 30
  memory_size     = 256

  environment {
    variables = {
      BASEPFAD     = "/tmp"
      KI_MODELL    = "gpt-4"
      BIST_OLLAMA  = "false"
      TABLE_NAME   = aws_dynamodb_table.alle_gesprache.name
    }
  }

  tags = merge(
    var.COMMON_TAGS,
    {
      Name        = "${var.ENV}-${each.key}"
      ENVironment = var.ENV
      Project     = "sprachweg"
      Handler     = each.key
    }
  )
}
