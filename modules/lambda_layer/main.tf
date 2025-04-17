# -------------------------------------
# Lambda Layer
# -------------------------------------
resource "aws_lambda_layer_version" "main" {
  filename            = local.lambda_functions_layer_path
  layer_name          = "${var.project_name}-${var.environment}-lambda-layer"
  compatible_runtimes = ["python3.13"]
  source_code_hash    = filebase64sha256(local.lambda_functions_layer_path)
}
