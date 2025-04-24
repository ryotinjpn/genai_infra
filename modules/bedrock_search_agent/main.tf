#######################################
# Bedrock Agent
#######################################
# AMAZON.UserInputの設定が必要な為、awsccを使用
resource "awscc_bedrock_agent" "main" {
  agent_name                  = "search-agent-${var.project_name}-${var.environment}"
  agent_resource_role_arn     = aws_iam_role.main.arn
  foundation_model            = "anthropic.claude-3-haiku-20240307-v1:0"
  idle_session_ttl_in_seconds = 600
  auto_prepare                = true
  instruction                 = local.instruction_prompt

  action_groups = [
    {
      action_group_name = "Search"
      action_group_executor = {
        lambda = var.lambda_function_arn
      }
      function_schema = {
        functions = [
          {
            name        = "search_news"
            description = local.search_news_description
          },
          {
            name        = "search_web"
            description = local.search_web_description
            parameters = {
              keyword = {
                type        = "string"
                description = "検索キーワード"
                required    = true
              }
            }
          }
        ]
      }
    },
    {
      # ユーザー入力を有効にする為に、UserInputActionは固定値必須
      action_group_name             = "UserInputAction"
      parent_action_group_signature = "AMAZON.UserInput"
    }
  ]
}

resource "aws_bedrockagent_agent_alias" "main" {
  agent_id         = awscc_bedrock_agent.main.id
  agent_alias_name = "latest"

  lifecycle {
    replace_triggered_by = [terraform_data.trigger.input]
  }
}

resource "terraform_data" "trigger" {
  input = local.agent_version
}


#######################################
# IAM
#######################################
resource "aws_iam_role" "main" {
  name               = "BedrockAgentRole-${var.project_name}-${var.environment}"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_iam_policy" "main" {
  name   = "BedrockAgentAccessForBedrock-${var.project_name}-${var.environment}"
  path   = "/service-role/"
  policy = data.aws_iam_policy_document.bedrock_role.json
}

resource "aws_iam_role_policy_attachment" "main" {
  role       = aws_iam_role.main.name
  policy_arn = aws_iam_policy.main.arn
}
