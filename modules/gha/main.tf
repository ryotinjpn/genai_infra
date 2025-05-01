#######################################
# IAM
#######################################
resource "aws_iam_openid_connect_provider" "main" {
  url            = "https://token.actions.githubusercontent.com"
  client_id_list = ["sts.amazonaws.com"]
}

resource "aws_iam_role" "pr_agent" {
  name               = "GHAPRAgentRole-${var.project_name}-${var.environment}"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_iam_policy" "pr_agent" {
  name   = "GHAPRAgentAccessForBedrock-${var.project_name}-${var.environment}"
  path   = "/service-role/"
  policy = data.aws_iam_policy_document.bedrock.json
}

resource "aws_iam_role_policy_attachment" "pr_agent" {
  role       = aws_iam_role.pr_agent.name
  policy_arn = aws_iam_policy.pr_agent.arn
}

resource "aws_iam_role" "deploy_lambda" {
  name               = "GHADeployLambdaRole-${var.project_name}-${var.environment}"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_iam_policy" "deploy_lambda" {
  name   = "GHADeployLambdaAccess-${var.project_name}-${var.environment}"
  path   = "/service-role/"
  policy = data.aws_iam_policy_document.lambda_deploy_policy.json
}

resource "aws_iam_role_policy_attachment" "deploy_lambda" {
  role       = aws_iam_role.deploy_lambda.name
  policy_arn = aws_iam_policy.deploy_lambda.arn
}
