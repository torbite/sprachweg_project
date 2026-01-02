# API Gateway REST API
resource "aws_apigatewayv2_api" "sprachweg_api" {
  name          = "${var.ENV}-sprachweg-api"
  protocol_type = "HTTP"
  description   = "API Gateway for Sprachweg handlers"

  tags = merge(
    var.COMMON_TAGS,
    {
      Name        = "${var.ENV}-sprachweg-api"
      ENVironment = var.ENV
      Project     = "sprachweg"
    }
  )
}

# API Gateway integration for test_handler
resource "aws_apigatewayv2_integration" "test_handler_integration" {
  api_id           = aws_apigatewayv2_api.sprachweg_api.id
  integration_type = "AWS_PROXY"

  integration_method = "POST"
  integration_uri    = aws_lambda_function.handler["test_handler"].invoke_arn
  payload_format_version = "2.0"
}

# API Gateway route for test_handler
resource "aws_apigatewayv2_route" "test_handler_route" {
  api_id    = aws_apigatewayv2_api.sprachweg_api.id
  route_key = "GET /test"
  target    = "integrations/${aws_apigatewayv2_integration.test_handler_integration.id}"
}

# Permission for API Gateway to invoke Lambda
resource "aws_lambda_permission" "test_handler_api_permission" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.handler["test_handler"].function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.sprachweg_api.execution_arn}/*/*"
}

# API Gateway stage
resource "aws_apigatewayv2_stage" "sprachweg_api_stage" {
  api_id      = aws_apigatewayv2_api.sprachweg_api.id
  name        = var.ENV
  auto_deploy = true

  tags = merge(
    var.COMMON_TAGS,
    {
      Name        = "${var.ENV}-sprachweg-api-stage"
      ENVironment = var.ENV
      Project     = "sprachweg"
    }
  )
}

# Output the API Gateway endpoint URL
output "api_gateway_id" {
  description = "API Gateway API ID"
  value       = aws_apigatewayv2_api.sprachweg_api.id
}

output "api_gateway_url" {
  description = "API Gateway endpoint URL"
  value       = aws_apigatewayv2_api.sprachweg_api.api_endpoint
}

output "api_gateway_invoke_url" {
  description = "API Gateway invoke URL (with stage)"
  value       = "${aws_apigatewayv2_api.sprachweg_api.api_endpoint}/${aws_apigatewayv2_stage.sprachweg_api_stage.name}"
}

output "test_handler_url" {
  description = "Test handler endpoint URL"
  value       = "${aws_apigatewayv2_api.sprachweg_api.api_endpoint}/${aws_apigatewayv2_stage.sprachweg_api_stage.name}/test"
}

