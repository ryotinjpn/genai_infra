#######################################
# IAM
#######################################
resource "aws_iam_openid_connect_provider" "main" {
  url            = "https://token.actions.githubusercontent.com"
  client_id_list = ["sts.amazonaws.com"]
}

resource "aws_iam_role" "main" {
  name               = "GHAPRAgentRole-${var.project_name}-${var.environment}"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_iam_policy" "main" {
  name   = "GHAPRAgentAccessForBedrock-${var.project_name}-${var.environment}"
  path   = "/service-role/"
  policy = data.aws_iam_policy_document.bedrock.json
}

resource "aws_iam_role_policy_attachment" "main" {
  role       = aws_iam_role.main.name
  policy_arn = aws_iam_policy.main.arn
}
