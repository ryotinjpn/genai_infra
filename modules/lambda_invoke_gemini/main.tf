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

  # ECRリポジトリにイメージがプッシュされた後に実行
  depends_on = [null_resource.docker_push]
}

#######################################
# ECR
#######################################
resource "aws_ecr_repository" "main" {
  name                 = "${var.project_name}/lambda_invoke_gemini"
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

resource "null_resource" "docker_push" {
  triggers = {
    always_run = "${timestamp()}"
  }
  provisioner "local-exec" {
    command = <<EOT
      aws ecr get-login-password --region ${data.aws_region.current.name} --profile ${data.aws_ssm_parameter.profile_name.value} | docker login --username AWS --password-stdin ${aws_ecr_repository.main.repository_url}
      docker tag ${aws_ecr_repository.main.name}:latest ${aws_ecr_repository.main.repository_url}:latest
      docker push ${aws_ecr_repository.main.repository_url}:latest
    EOT
  }
  # ECRリポジトリの作成後に実行
  depends_on = [aws_ecr_repository.main]
}

resource "null_resource" "lambda_update_function_code" {
  triggers = {
    always_run = "${timestamp()}"
  }
  provisioner "local-exec" {
    command = <<EOT
      aws lambda update-function-code --function-name ${aws_lambda_function.main.function_name} --image-uri ${aws_ecr_repository.main.repository_url}:latest --region ${data.aws_region.current.name} --profile ${data.aws_ssm_parameter.profile_name.value}
    EOT
  }
  # Lambda関数の作成後に実行
  depends_on = [aws_lambda_function.main]
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
