variable "table_name" {
  description = "Name of the DynamoDB table for conversations"
  type        = string
  default     = "alle_gesprache"
}

variable "billing_mode" {
  description = "DynamoDB billing mode - PAY_PER_REQUEST or PROVISIONED"
  type        = string
  default     = "PAY_PER_REQUEST"
}

variable "enable_point_in_time_recovery" {
  description = "Enable point-in-time recovery for the DynamoDB table"
  type        = bool
  default     = true
}

variable "env" {
  description = "Environment name (e.g., dev, staging, prod). Should be set via TF_VAR_ENV environment variable from .env file"
  type        = string
  default     = "dev"
}

variable "common_tags" {
  description = "Common tags to apply to all resources"
  type        = map(string)
  default     = {}
}

