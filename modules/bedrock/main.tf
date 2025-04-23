#######################################
# Bedrock Agent
#######################################
# AMAZON.UserInputの設定が必要な為、awsccを使用
resource "awscc_bedrock_agent" "main" {
  agent_name                  = "bedrock_agent"
  agent_resource_role_arn     = aws_iam_role.main.arn
  foundation_model            = "anthropic.claude-3-haiku-20240307-v1:0"
  idle_session_ttl_in_seconds = 600
  auto_prepare                = true
  instruction                 = local.prompt

  action_groups = [
    {
      action_group_name = "BedrockAgentAPIAction"
      action_group_executor = {
        lambda = var.lambda_function_arn
      }
      function_schema = {
        functions = [
          {
            name        = "get_available_vacations_days"
            description = "get the number of vacations available for a certain employee"
            parameters = {
              employee_id = {
                type        = "integer"
                description = "the id of the employee to get the available vacations"
                required    = true
              }
            }
          },
          {
            name        = "reserve_vacation_time"
            description = "reserve vacation time for a specific employee - you need all parameters to reserve vacation time"
            parameters = {
              employee_id = {
                type        = "integer"
                description = "the id of the employee"
                required    = true
              }
              start_date = {
                type        = "string"
                description = "the start date for the vacation"
                required    = true
              }
              end_date = {
                type        = "string"
                description = "the end date for the vacation"
                required    = true
              }
            }
          }
        ]
      }
    },
    {
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
