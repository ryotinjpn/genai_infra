data "aws_caller_identity" "self" {}
data "aws_region" "current" {}


#######################################
# IAM
#######################################
data "aws_iam_policy_document" "assume_role" {
  statement {
    actions = ["sts:AssumeRole"]
    effect  = "Allow"
    principals {
      type        = "Service"
      identifiers = ["bedrock.amazonaws.com"]
    }
    condition {
      test     = "StringEquals"
      variable = "aws:SourceAccount"
      values   = [data.aws_caller_identity.self.id]
    }
    condition {
      test     = "ArnLike"
      variable = "aws:SourceArn"
      values   = ["arn:aws:bedrock:${data.aws_region.current.name}:${data.aws_caller_identity.self.id}:agent/*"]
    }
  }
}

data "aws_iam_policy_document" "bedrock_role" {
  version = "2012-10-17"
  statement {
    effect = "Allow"
    actions = [
      "bedrock:InvokeModel",
      "bedrock:InvokeModelWithResponseStream"
    ]
    resources = [
      "arn:aws:bedrock:*::foundation-model/anthropic.*",
      "arn:aws:bedrock:${data.aws_region.current.name}:${data.aws_caller_identity.self.id}:inference-profile/*"
    ]
  }
}
