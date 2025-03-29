module "lambda_generate_post_to_x" {
  source = "../../modules/lambda_generate_post_to_x"

  project_name = local.project_name
  environment  = local.environment

  bedrock_region      = local.bedrock_region
  model_id            = local.model_id
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
