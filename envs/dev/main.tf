module "lambda_common" {
  source = "../../modules/lambda_common"

  project_name = local.project_name
  environment  = local.environment

  lambda_runtime_python = local.lambda_runtime_python
}

module "lambda_generate_post_to_x" {
  source = "../../modules/lambda_generate_post_to_x"

  project_name = local.project_name
  environment  = local.environment

  bedrock_region        = local.bedrock_region
  model_id              = local.model_id
  lambda_runtime_python = local.lambda_runtime_python
  lambda_layer_arn      = module.lambda_common.lambda_layer_arn
  sns_topic_arn         = module.lambda_common.sns_topic_arn
  dynamodb_table_name   = module.dynamodb.generate_post_to_x_name
}

module "lambda_generate_message_to_line" {
  source = "../../modules/lambda_generate_message_to_line"

  project_name = local.project_name
  environment  = local.environment

  bedrock_region        = local.bedrock_region
  model_id              = local.model_id
  lambda_runtime_python = local.lambda_runtime_python
  lambda_layer_arn      = module.lambda_common.lambda_layer_arn
  sns_topic_arn         = module.lambda_common.sns_topic_arn
}

module "lambda_webhook_to_line" {
  source = "../../modules/lambda_webhook_to_line"

  project_name = local.project_name
  environment  = local.environment

  bedrock_region        = local.bedrock_region
  model_id              = local.model_id
  lambda_runtime_python = local.lambda_runtime_python
  lambda_layer_arn      = module.lambda_common.lambda_layer_arn
  sns_topic_arn         = module.lambda_common.sns_topic_arn
}

module "dynamodb" {
  source = "../../modules/dynamodb"
}

module "gha" {
  source = "../../modules/gha"

  project_name = local.project_name
  environment  = local.environment

  bedrock_region = local.bedrock_region
}
