data "aws_caller_identity" "self" {}
data "aws_region" "current" {}

# -------------------------------------
# Lambda Function
# -------------------------------------
data "archive_file" "main" {
  type        = "zip"
  source_file = local.lambda_functions_path
  output_path = local.lambda_zip_path
  depends_on  = [aws_lambda_layer_version.main]
}

# -------------------------------------
# IAM
# -------------------------------------
data "aws_iam_policy_document" "lambda_assume_role" {
  version = "2012-10-17"
  statement {
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}

data "aws_iam_policy_document" "lambda_role" {
  version = "2012-10-17"
  statement {
    effect = "Allow"
    actions = [
      "ssm:GetParameter",
      "ssm:GetParameters",
      "ssm:PutParameter",
    ]
    resources = [
      "arn:aws:ssm:${data.aws_region.current.name}:${data.aws_caller_identity.self.id}:parameter/*",
    ]
  }
  statement {
    effect = "Allow"
    actions = [
      "kms:Decrypt"
    ]
    resources = [
      "arn:aws:kms:${data.aws_region.current.name}:${data.aws_caller_identity.self.id}:key/*"
    ]
  }
  statement {
    effect = "Allow"
    actions = [
      "logs:CreateLogStream",
      "logs:PutLogEvents",
    ]
    resources = ["arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.self.id}:log-group:/aws/lambda/${aws_lambda_function.main.function_name}:*"]
  }
  statement {
    effect = "Allow"
    actions = [
      "dynamodb:Scan",
      "dynamodb:PutItem",
    ]
    resources = ["arn:aws:dynamodb:${data.aws_region.current.name}:${data.aws_caller_identity.self.id}:table/${var.dynamodb_table_name}"]
  }
  statement {
    effect = "Allow"
    actions = [
      "bedrock:InvokeModel",
    ]
    resources = [
      "arn:aws:bedrock:*::foundation-model/anthropic.*",
      "arn:aws:bedrock:${var.bedrock_region}:${data.aws_caller_identity.self.id}:inference-profile/*"
    ]
  }
}
