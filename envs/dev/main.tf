module "lambda_common" {
  source = "../../modules/lambda_common"

  project_name = local.project_name
  environment  = local.environment

  lambda_runtime_python = local.lambda_runtime_python
}

module "bedrock_search_agent" {
  source = "../../modules/bedrock_search_agent"

  providers = {
    awscc = awscc.virginia
  }

  project_name = local.project_name
  environment  = local.environment

  lambda_function_arn = module.lambda_search_agent.lambda_function_arn
}

module "lambda_search_agent" {
  source = "../../modules/lambda_search_agent"

  project_name = local.project_name
  environment  = local.environment

  lambda_runtime_python   = local.lambda_runtime_python
  lambda_layer_common_arn = module.lambda_common.lambda_layer_common_arn
  sns_topic_arn           = module.lambda_common.sns_topic_arn
}

module "bedrock_google_calendar_agent" {
  source = "../../modules/bedrock_google_calendar_agent"

  providers = {
    awscc = awscc.virginia
  }

  project_name = local.project_name
  environment  = local.environment

  lambda_function_arn = module.lambda_google_calendar_agent.lambda_function_arn
}

module "lambda_google_calendar_agent" {
  source = "../../modules/lambda_google_calendar_agent"

  project_name = local.project_name
  environment  = local.environment

  model_id                = local.model_id
  lambda_runtime_python   = local.lambda_runtime_python
  lambda_layer_common_arn = module.lambda_common.lambda_layer_common_arn
  lambda_layer_gcp_arn    = module.lambda_common.lambda_layer_gcp_arn
  sns_topic_arn           = module.lambda_common.sns_topic_arn
}

module "lambda_generate_post_to_x" {
  source = "../../modules/lambda_generate_post_to_x"

  project_name = local.project_name
  environment  = local.environment

  model_id                = local.model_id
  lambda_runtime_python   = local.lambda_runtime_python
  lambda_layer_common_arn = module.lambda_common.lambda_layer_common_arn
  sns_topic_arn           = module.lambda_common.sns_topic_arn
  dynamodb_table_name     = module.dynamodb.generate_post_to_x_name
}

module "lambda_generate_message_to_line" {
  source = "../../modules/lambda_generate_message_to_line"

  project_name = local.project_name
  environment  = local.environment

  model_id                = local.model_id
  lambda_runtime_python   = local.lambda_runtime_python
  lambda_layer_common_arn = module.lambda_common.lambda_layer_common_arn
  sns_topic_arn           = module.lambda_common.sns_topic_arn
}

module "lambda_webhook_to_line" {
  source = "../../modules/lambda_webhook_to_line"

  project_name = local.project_name
  environment  = local.environment

  model_id                = local.model_id
  lambda_runtime_python   = local.lambda_runtime_python
  lambda_layer_common_arn = module.lambda_common.lambda_layer_common_arn
  sns_topic_arn           = module.lambda_common.sns_topic_arn
  bedrock_agent_id        = module.bedrock_search_agent.bedrock_agent_id
  bedrock_agent_alias_id  = module.bedrock_search_agent.bedrock_agent_alias_id
}

module "lambda_invoke_bedrock_agent" {
  source = "../../modules/lambda_invoke_bedrock_agent"

  project_name = local.project_name
  environment  = local.environment

  lambda_runtime_python   = local.lambda_runtime_python
  lambda_layer_common_arn = module.lambda_common.lambda_layer_common_arn
  sns_topic_arn           = module.lambda_common.sns_topic_arn
}

module "lambda_invoke_gemini" {
  source = "../../modules/lambda_invoke_gemini"

  project_name = local.project_name
  environment  = local.environment

  gcp_project_id = local.gcp_project_id
  sns_topic_arn  = module.lambda_common.sns_topic_arn
}

module "dynamodb" {
  source = "../../modules/dynamodb"
}

module "gha" {
  source = "../../modules/gha"

  project_name = local.project_name
  environment  = local.environment
}

module "service_account" {
  source = "../../modules/service_account"

  project_name = local.project_name
  environment  = local.environment
}
