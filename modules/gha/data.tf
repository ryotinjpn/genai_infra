data "aws_caller_identity" "self" {}
data "aws_region" "current" {}

#######################################
# IAM
#######################################
data "aws_iam_policy_document" "assume_role" {
  version = "2012-10-17"
  statement {
    actions = ["sts:AssumeRoleWithWebIdentity"]
    effect  = "Allow"

    principals {
      type        = "Federated"
      identifiers = [aws_iam_openid_connect_provider.main.arn]
    }

    condition {
      test     = "StringEquals"
      variable = "token.actions.githubusercontent.com:aud"
      values   = ["sts.amazonaws.com"]
    }

    condition {
      test     = "StringLike"
      variable = "token.actions.githubusercontent.com:sub"
      values   = ["repo:ryotinjpn/*"]
    }
  }
}

data "aws_iam_policy_document" "bedrock" {
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
