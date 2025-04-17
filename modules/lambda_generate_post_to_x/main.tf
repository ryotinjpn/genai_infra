# -------------------------------------
# Lambda Layer
# -------------------------------------
resource "aws_lambda_layer_version" "main" {
  filename            = local.lambda_functions_layer_path
  layer_name          = "${var.project_name}-${var.environment}-lambda-layer"
  compatible_runtimes = ["python3.13"]
  source_code_hash    = filebase64sha256(local.lambda_functions_layer_path)
}

# -------------------------------------
# Lambda Function
# -------------------------------------
resource "aws_lambda_function" "main" {
  function_name    = "${var.project_name}-${var.environment}-generate-post-to-x"
  description      = "Xの投稿内容を自動生成し投稿する Lambda 関数"
  handler          = "lambda_handler.lambda_handler"
  memory_size      = 128
  timeout          = 900
  runtime          = "python3.13"
  role             = aws_iam_role.main.arn
  filename         = local.lambda_zip_path
  source_code_hash = data.archive_file.main.output_base64sha256
  layers = [
    aws_lambda_layer_version.main.arn,
    "arn:aws:lambda:ap-northeast-1:133490724326:layer:AWS-Parameters-and-Secrets-Lambda-Extension:11"
  ]
  environment {
    variables = {
      TZ                  = "Asia/Tokyo"
      MODEL_ID            = var.model_id
      X_API_CLIENT_ID     = "/${var.project_name}/${var.environment}/X_API_CLIENT_ID"
      X_API_CLIENT_SECRET = "/${var.project_name}/${var.environment}/X_API_CLIENT_SECRET"
      X_API_REFRESH_TOKEN = "/${var.project_name}/${var.environment}/X_API_REFRESH_TOKEN"
    }
  }
}

# -------------------------------------
# Lambda Permission
# -------------------------------------
resource "aws_lambda_permission" "main" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.main.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.main.arn
}

# -------------------------------------
# EventBridge
# -------------------------------------
resource "aws_cloudwatch_event_rule" "main" {
  name                = "notice-generate-post-to-x-jst-1100"
  description         = "11:00 の時間検知 Event をトリガーに Lambda function (${aws_lambda_function.main.function_name}) を起動"
  schedule_expression = "cron(0 2 * * ? *)"
}

resource "aws_cloudwatch_event_target" "main" {
  rule = aws_cloudwatch_event_rule.main.name
  arn  = aws_lambda_function.main.arn
}

# -------------------------------------
# CloudWatch Logs
# -------------------------------------
resource "aws_cloudwatch_log_group" "main" {
  name              = "/aws/lambda/${aws_lambda_function.main.function_name}"
  retention_in_days = 30
}

# -------------------------------------
# IAM
# -------------------------------------
resource "aws_iam_role" "main" {
  name               = "LambdaRoleForCreatePostToX-${var.project_name}-${var.environment}"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}

resource "aws_iam_role_policy_attachment" "main" {
  role       = aws_iam_role.main.name
  policy_arn = aws_iam_policy.main.arn
}

resource "aws_iam_policy" "main" {
  name   = "LambdaAccessForCreatePostToX-${var.project_name}-${var.environment}"
  policy = data.aws_iam_policy_document.lambda_role.json
}
