module "lambda_layer" {
  source = "../../modules/lambda_layer"

  project_name = local.project_name
  environment  = local.environment
}

module "lambda_generate_post_to_x" {
  source = "../../modules/lambda_generate_post_to_x"

  project_name = local.project_name
  environment  = local.environment

  bedrock_region      = local.bedrock_region
  model_id            = local.model_id
  lambda_layer_arn    = module.lambda_layer.lambda_layer_arn
  dynamodb_table_name = module.dynamodb.generate_post_to_x_name
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
