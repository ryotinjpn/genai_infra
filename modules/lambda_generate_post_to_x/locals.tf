locals {
  lambda_functions_root_path = "../../functions"
  lambda_source_dir          = "${local.lambda_functions_root_path}/generate_post_to_x/src"
  lambda_zip_path            = "${local.lambda_functions_root_path}/generate_post_to_x/lambda.zip"
}
