locals {
  project_name = "genai"
  environment  = "dev"

  gcp_project_id = "vertex-ai-ryotinjpn"

  model_id              = "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
  lambda_runtime_python = "python3.13"
}
