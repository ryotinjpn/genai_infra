module "lambda_generate_post_to_x" {
  source = "../../modules/lambda_generate_post_to_x"

  project_name = local.project_name
  environment  = local.environment

  bedrock_region = local.bedrock_region
  model_id       = local.model_id
}

module "gha" {
  source = "../../modules/gha"

  project_name = local.project_name
  environment  = local.environment
}
