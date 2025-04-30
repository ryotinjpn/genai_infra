locals {
  lambda_layers_path           = "../../lambda_layers"
  lambda_layers_common_path    = "${local.lambda_layers_path}/common/lambda_layer.zip"
  lambda_layers_layer_gcp_path = "${local.lambda_layers_path}/gcp/lambda_layer.zip"
}
