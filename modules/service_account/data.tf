data "google_project" "current" {}

data "aws_caller_identity" "self" {}
data "aws_ssm_parameter" "project_number" {
  name = "/${var.project_name}/${var.environment}/GCP_PROJECT_NUMBER"
}
