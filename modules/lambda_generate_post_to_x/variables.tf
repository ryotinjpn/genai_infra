#######################################
# Common
#######################################
variable "project_name" {
  type        = string
  description = "Enter the Project Name."
  nullable    = false
}

variable "environment" {
  description = "Enter the Environment."
  type        = string
  nullable    = false
  validation {
    condition     = contains(["sandbox", "dev", "stg", "prd"], var.environment)
    error_message = "environment must be one of the following: [sandbox, dev, stg, prd]."
  }
}

#######################################
# Lambda
#######################################
variable "bedrock_region" {
  type        = string
  description = "Enter the Bedrock Region."
  nullable    = false
}

variable "model_id" {
  type        = string
  description = "Enter the Model ID."
  nullable    = false
}

variable "lambda_runtime_python" {
  type        = string
  description = "Enter the Lambda Runtime Python."
  nullable    = false
}

variable "lambda_layer_arn" {
  type        = string
  description = "Enter the Lambda Layer Arn."
  nullable    = false
}

variable "sns_topic_arn" {
  type        = string
  description = "Enter the SNS Topic Arn."
  nullable    = false
}

variable "dynamodb_table_name" {
  type        = string
  description = "Enter the DynamoDB Table Name."
  nullable    = false
}
