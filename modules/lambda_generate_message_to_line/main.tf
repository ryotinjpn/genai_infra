# -------------------------------------
# Lambda Function
# -------------------------------------
resource "aws_lambda_function" "main" {
  function_name    = "${var.project_name}-${var.environment}-generate-message-to-line"
  description      = "LINEへプッシュメッセージを送信する Lambda 関数"
  handler          = "lambda_handler.lambda_handler"
  memory_size      = 128
  timeout          = 900
  runtime          = var.lambda_runtime_python
  role             = aws_iam_role.main.arn
  filename         = local.lambda_zip_path
  source_code_hash = data.archive_file.main.output_base64sha256
  layers = [
    var.lambda_layer_arn,
    "arn:aws:lambda:ap-northeast-1:133490724326:layer:AWS-Parameters-and-Secrets-Lambda-Extension:11"
  ]
  environment {
    variables = {
      TZ                            = "Asia/Tokyo"
      MODEL_ID                      = var.model_id
      BRAVE_API_KEY                 = "/${var.project_name}/${var.environment}/BRAVE_API_KEY"
      LINE_API_CHANNEL_ACCESS_TOKEN = "/${var.project_name}/${var.environment}/LINE_API_CHANNEL_ACCESS_TOKEN"
      LINE_API_TARGET_ID            = "/${var.project_name}/${var.environment}/LINE_API_TARGET_ID"
    }
  }
}

# -------------------------------------
# Lambda Permission
# -------------------------------------
resource "aws_lambda_permission" "eight_am" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.main.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.eight_am.arn
}

resource "aws_lambda_permission" "five_pm" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.main.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.five_pm.arn
}

# -------------------------------------
# EventBridge
# -------------------------------------
resource "aws_cloudwatch_event_rule" "eight_am" {
  name                = "notice-generate-message-to-line-jst-8-am"
  description         = "AM8:00 の時間検知 Event をトリガーに Lambda function (${aws_lambda_function.main.function_name}) を起動"
  schedule_expression = "cron(0 23 * * ? *)"
}

resource "aws_cloudwatch_event_target" "eight_am" {
  rule = aws_cloudwatch_event_rule.eight_am.name
  arn  = aws_lambda_function.main.arn
}

resource "aws_cloudwatch_event_rule" "five_pm" {
  name                = "notice-generate-message-to-line-jst-5-pm"
  description         = "PM5:00 の時間検知 Event をトリガーに Lambda function (${aws_lambda_function.main.function_name}) を起動"
  schedule_expression = "cron(0 8 * * ? *)"
}

resource "aws_cloudwatch_event_target" "five_pm" {
  rule = aws_cloudwatch_event_rule.five_pm.name
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
  name               = "LambdaRoleForGenerateMessageToLine-${var.project_name}-${var.environment}"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}

resource "aws_iam_role_policy_attachment" "main" {
  role       = aws_iam_role.main.name
  policy_arn = aws_iam_policy.main.arn
}

resource "aws_iam_policy" "main" {
  name   = "LambdaRoleForGenerateMessageToLine-${var.project_name}-${var.environment}"
  policy = data.aws_iam_policy_document.lambda_role.json
}
