locals {
  lambda_functions_root_path = "../../functions"
  lambda_source_dir          = "${local.lambda_functions_root_path}/invoke_bedrock_agent/src"
  lambda_zip_path            = "${local.lambda_functions_root_path}/invoke_bedrock_agent/lambda.zip"
}
