variable "TABLE_NAME" {
  description = "Name of the DynamoDB table for conversations"
  type        = string
  default     = "alle_gesprache"
}

variable "BILLING_MODE" {
  description = "DynamoDB billing mode - PAY_PER_REQUEST or PROVISIONED"
  type        = string
  default     = "PAY_PER_REQUEST"
}

variable "ENABLE_POINT_IN_TIME_RECOVERY" {
  description = "Enable point-in-time recovery for the DynamoDB table"
  type        = bool
  default     = true
}

variable "ENV" {
  description = "Environment name (e.g., dev, staging, prod). Must be set via TF_VAR_ENV environment variable from .env file"
  type        = string
}

variable "COMMON_TAGS" {
  description = "Common tags to apply to all resources"
  type        = map(string)
  default     = {}
}

