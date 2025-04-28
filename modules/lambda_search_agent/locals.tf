locals {
  lambda_functions_root_path = "../../functions"
  lambda_source_dir          = "${local.lambda_functions_root_path}/search_agent/src"
  lambda_zip_path            = "${local.lambda_functions_root_path}/search_agent/lambda.zip"
  model_id                   = "anthropic.claude-3-haiku-20240307-v1:0"
}
