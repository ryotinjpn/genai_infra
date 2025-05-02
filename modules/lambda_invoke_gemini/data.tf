data "aws_caller_identity" "self" {}
data "aws_region" "current" {}

#######################################
# ECR
#######################################
data "aws_ecr_lifecycle_policy_document" "main" {
  rule {
    priority    = 1
    description = "life cycle for untagged images"
    selection {
      tag_status   = "untagged"
      count_type   = "imageCountMoreThan"
      count_number = 1
    }
    action {
      type = "expire"
    }
  }
}

#######################################
# IAM
#######################################
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
    ]
    resources = [
      "arn:aws:ssm:${data.aws_region.current.name}:${data.aws_caller_identity.self.id}:parameter/*",
    ]
  }
  statement {
    effect = "Allow"
    actions = [
      "kms:Decrypt",
      "kms:Encrypt",
      "kms:GenerateDataKey",
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
      "sns:Publish",
    ]
    resources = [var.sns_topic_arn]
  }
}
