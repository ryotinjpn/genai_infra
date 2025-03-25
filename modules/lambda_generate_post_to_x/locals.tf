locals {
  lambda_functions_root_path  = "../../functions"
  lambda_functions_layer_path = "${local.lambda_functions_root_path}/lambda_layer.zip"
  lambda_functions_path       = "${local.lambda_functions_root_path}/generate_post_to_x/lambda_function.py"
  lambda_zip_path             = "${local.lambda_functions_root_path}/generate_post_to_x/lambda_function.zip"
}
