locals {
  project_id     = data.google_project.current.project_id
  project_number = data.aws_ssm_parameter.project_number.value
  services = toset([
    "iam.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "iamcredentials.googleapis.com",
    "sts.googleapis.com",
    "aiplatform.googleapis.com"
  ])
}
