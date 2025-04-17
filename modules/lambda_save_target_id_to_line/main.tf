# -------------------------------------
# Lambda Function
# -------------------------------------
resource "aws_lambda_function" "main" {
  function_name    = "${var.project_name}-${var.environment}-save-target-id-to-line"
  description      = "LINE API Webhookから送信先IDを取得する Lambda 関数"
  handler          = "lambda_handler.lambda_handler"
  memory_size      = 128
  timeout          = 900
  runtime          = "python3.13"
  role             = aws_iam_role.main.arn
  filename         = local.lambda_zip_path
  source_code_hash = data.archive_file.main.output_base64sha256
  layers = [
    var.lambda_layer_arn,
    "arn:aws:lambda:ap-northeast-1:133490724326:layer:AWS-Parameters-and-Secrets-Lambda-Extension:11"
  ]
  environment {
    variables = {
      TZ                 = "Asia/Tokyo"
      LINE_API_TARGET_ID = "/${var.project_name}/${var.environment}/LINE_API_TARGET_ID"
    }
  }
}

resource "aws_lambda_function_url" "main" {
  function_name      = aws_lambda_function.main.function_name
  authorization_type = "NONE"
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
  name               = "LambdaRoleForSaveTargetIdToLine-${var.project_name}-${var.environment}"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}

resource "aws_iam_role_policy_attachment" "main" {
  role       = aws_iam_role.main.name
  policy_arn = aws_iam_policy.main.arn
}

resource "aws_iam_policy" "main" {
  name   = "LambdaRoleForSaveTargetIdToLine-${var.project_name}-${var.environment}"
  policy = data.aws_iam_policy_document.lambda_role.json
}
