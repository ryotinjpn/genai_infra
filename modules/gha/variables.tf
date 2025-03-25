# -------------------------------------
# Common
# -------------------------------------
variable "project_name" {
  type        = string
  description = "Enter the project name."
  nullable    = false
}

variable "environment" {
  description = "Enter the environment."
  type        = string
  nullable    = false
  validation {
    condition     = contains(["sandbox", "dev", "stg", "prd"], var.environment)
    error_message = "environment must be one of the following: [sandbox, dev, stg, prd]."
  }
}

# -------------------------------------
# IAM
# -------------------------------------
variable "bedrock_region" {
  type        = string
  description = "Enter the Bedrock region."
  nullable    = false
}
