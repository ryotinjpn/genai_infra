#######################################
# Lambda Function
#######################################
resource "aws_lambda_function" "main" {
  function_name    = "${var.project_name}-${var.environment}-invoke-search-agent"
  description      = "Search Agent の 呼び出しテスト用 Lambda 関数"
  handler          = "lambda_handler.lambda_handler"
  memory_size      = 128
  timeout          = 900
  runtime          = var.lambda_runtime_python
  role             = aws_iam_role.main.arn
  filename         = local.lambda_zip_path
  source_code_hash = data.archive_file.main.output_base64sha256
  layers = [
    var.lambda_layer_arn
  ]
  environment {
    variables = {
      TZ                     = "Asia/Tokyo"
      BEDROCK_AGENT_ID       = var.bedrock_agent_id
      BEDROCK_AGENT_ALIAS_ID = var.bedrock_agent_alias_id
      SNS_TOPIC_ARN          = var.sns_topic_arn
    }
  }
}

#######################################
# CloudWatch Logs
#######################################
resource "aws_cloudwatch_log_group" "main" {
  name              = "/aws/lambda/${aws_lambda_function.main.function_name}"
  retention_in_days = 30
}

#######################################
# IAM
#######################################
resource "aws_iam_role" "main" {
  name               = "LambdaRoleForInvokeSearchAgent-${var.project_name}-${var.environment}"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}

resource "aws_iam_role_policy_attachment" "main" {
  role       = aws_iam_role.main.name
  policy_arn = aws_iam_policy.main.arn
}

resource "aws_iam_policy" "main" {
  name   = "LambdaRoleForInvokeSearchAgent-${var.project_name}-${var.environment}"
  policy = data.aws_iam_policy_document.lambda_role.json
}
