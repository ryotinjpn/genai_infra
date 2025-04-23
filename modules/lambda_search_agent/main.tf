#######################################
# Lambda Function
#######################################
resource "aws_lambda_function" "main" {
  function_name    = "${var.project_name}-${var.environment}-search-agent"
  description      = "Search Agentの アクショングループで起動する Lambda 関数"
  handler          = "lambda_handler.lambda_handler"
  memory_size      = 128
  timeout          = 900
  runtime          = var.lambda_runtime_python
  role             = aws_iam_role.main.arn
  filename         = local.lambda_zip_path
  source_code_hash = data.archive_file.main.output_base64sha256
  layers = [
    var.lambda_layer_arn,
  ]
  environment {
    variables = {
      TZ            = "Asia/Tokyo"
      BRAVE_API_KEY = "/${var.project_name}/${var.environment}/BRAVE_API_KEY"
      SNS_TOPIC_ARN = var.sns_topic_arn
    }
  }
}

#######################################
# Lambda Permission
#######################################
resource "aws_lambda_permission" "main" {
  statement_id   = "AllowExecutionFromBedrock"
  action         = "lambda:InvokeFunction"
  function_name  = aws_lambda_function.main.function_name
  principal      = "bedrock.amazonaws.com"
  source_account = data.aws_caller_identity.self.id
  source_arn     = "arn:aws:bedrock:${data.aws_region.current.name}:${data.aws_caller_identity.self.id}:agent/*"
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
  name               = "LambdaRoleForBedrockAgent-${var.project_name}-${var.environment}"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}

resource "aws_iam_role_policy_attachment" "main" {
  role       = aws_iam_role.main.name
  policy_arn = aws_iam_policy.main.arn
}

resource "aws_iam_policy" "main" {
  name   = "LambdaRoleForBedrockAgent-${var.project_name}-${var.environment}"
  policy = data.aws_iam_policy_document.lambda_role.json
}
