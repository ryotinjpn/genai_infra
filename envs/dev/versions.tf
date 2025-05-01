terraform {
  required_version = "1.10.5"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "5.95.0"
    }

    awscc = {
      source  = "hashicorp/awscc"
      version = "1.37.0"
    }

    google = {
      source  = "hashicorp/google"
      version = "6.33.0"
    }
  }
}
