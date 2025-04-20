locals {
  project_name = "genai"
  environment  = "dev"

  bedrock_region        = "us-east-1"
  model_id              = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
  lambda_runtime_python = "python3.13"
}
