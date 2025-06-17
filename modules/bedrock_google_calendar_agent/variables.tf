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
variable "lambda_function_arn" {
  type        = string
  description = "Enter the Lambda Function Arn."
  nullable    = false
}
