#######################################
# Lambda Layer
#######################################
resource "aws_lambda_layer_version" "common" {
  filename            = local.lambda_layers_common_path
  layer_name          = "${var.project_name}-${var.environment}-lambda-layer-common"
  compatible_runtimes = [var.lambda_runtime_python]
  source_code_hash    = filebase64sha256(local.lambda_layers_common_path)
}

#######################################
# SNS Topic
#######################################
resource "aws_sns_topic" "main" {
  name              = "${var.project_name}-${var.environment}-lambda"
  kms_master_key_id = aws_kms_key.sns.arn
}

resource "aws_sns_topic_subscription" "main" {
  topic_arn = aws_sns_topic.main.arn
  protocol  = "email"
  endpoint  = "ryotinjpn@gmail.com"
}

#######################################
# KMS
#######################################
resource "aws_kms_key" "sns" {
  description             = "KMS key for encrypting SNS"
  deletion_window_in_days = 30
  enable_key_rotation     = true
  policy                  = data.aws_iam_policy_document.sns_kms_key.json
}

resource "aws_kms_alias" "sns" {
  name          = "alias/cmk/${var.project_name}-${var.environment}-sns"
  target_key_id = aws_kms_key.sns.key_id
}
