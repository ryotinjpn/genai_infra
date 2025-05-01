#######################################
# Lambda Function
#######################################
resource "aws_lambda_function" "main" {
  function_name = "${var.project_name}-${var.environment}-invoke-gemini"
  description   = "Gemini 呼び出し用 Lambda 関数"
  package_type  = "Image"
  image_uri     = "${aws_ecr_repository.main.repository_url}:latest"
  memory_size   = 512
  timeout       = 900
  role          = aws_iam_role.main.arn
  environment {
    variables = {
      TZ                                  = "Asia/Tokyo"
      MODEL_ID                            = "gemini-2.5-flash-preview-04-17"
      GOOGLE_APPLICATION_CREDENTIALS_PATH = "/${var.project_name}/${var.environment}/GOOGLE_APPLICATION_CREDENTIALS"
      GCP_PROJECT_ID                      = var.gcp_project_id
      SNS_TOPIC_ARN                       = var.sns_topic_arn
    }
  }
}

#######################################
# ECR
#######################################
resource "aws_ecr_repository" "main" {
  name                 = "${var.project_name}/${var.environment}/lambda_invoke_gemini"
  image_tag_mutability = "MUTABLE"
  image_scanning_configuration {
    scan_on_push = true
  }
  force_delete = true
}

resource "aws_ecr_lifecycle_policy" "main" {
  repository = aws_ecr_repository.main.name
  policy     = data.aws_ecr_lifecycle_policy_document.main.json
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
  name               = "LambdaRoleForInvokeGemini-${var.project_name}-${var.environment}"
  assume_role_policy = data.aws_iam_policy_document.lambda_assume_role.json
}

resource "aws_iam_role_policy_attachment" "main" {
  role       = aws_iam_role.main.name
  policy_arn = aws_iam_policy.main.arn
}

resource "aws_iam_policy" "main" {
  name   = "LambdaRoleForInvokeGemini-${var.project_name}-${var.environment}"
  policy = data.aws_iam_policy_document.lambda_role.json
}
