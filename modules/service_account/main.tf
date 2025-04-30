#######################################
# Service Account
#######################################
## API の 有効化
resource "google_project_service" "main" {
  for_each                   = local.services
  project                    = local.project_id
  service                    = each.value
  disable_dependent_services = true
}

resource "google_service_account" "aws_sa" {
  project      = local.project_id
  account_id   = local.project_id
  display_name = local.project_id
}

#######################################
# Workload Identity
#######################################
resource "google_iam_workload_identity_pool" "aws_id_pool" {
  project                   = local.project_id
  workload_identity_pool_id = "aws-${var.project_name}-${var.environment}"
  display_name              = "aws-${var.project_name}-${var.environment}"
  description               = "AWS用 IDプール"
}

resource "google_iam_workload_identity_pool_provider" "aws_sa" {
  workload_identity_pool_id          = google_iam_workload_identity_pool.aws_id_pool.workload_identity_pool_id
  workload_identity_pool_provider_id = "aws-${var.project_name}-${var.environment}"
  display_name                       = "aws-${var.project_name}-${var.environment}"
  description                        = "AWS用 プロバイダ"
  aws {
    account_id = data.aws_caller_identity.self.id
  }
}

#######################################
# IAM
#######################################
# サービスアカウントにVertex AI権限付与
resource "google_project_iam_member" "aws_sa_role" {
  project = local.project_id
  role    = "roles/aiplatform.user"
  member  = "serviceAccount:${google_service_account.aws_sa.email}"
}

# AWSがサービスアカウントの権限借用許可
resource "google_service_account_iam_binding" "aws_sa_role_binging" {
  service_account_id = google_service_account.aws_sa.name
  role               = "roles/iam.workloadIdentityUser"

  members = [
    "principalSet://iam.googleapis.com/projects/${local.project_number}/locations/global/workloadIdentityPools/${google_iam_workload_identity_pool.aws_id_pool.workload_identity_pool_id}/*",
  ]
}
