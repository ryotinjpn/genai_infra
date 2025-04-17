locals {
  lambda_functions_root_path = "../../functions"
  lambda_source_dir          = "${local.lambda_functions_root_path}/save_target_id_to_line/src"
  lambda_zip_path            = "${local.lambda_functions_root_path}/save_target_id_to_line/lambda.zip"
}
