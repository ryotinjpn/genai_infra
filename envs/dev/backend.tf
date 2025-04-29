terraform {
  backend "s3" {
    bucket       = "tfstate-genai-dev-us-east-1"
    key          = "terraform-playground.tfstate"
    region       = "us-east-1"
    encrypt      = true
    use_lockfile = true
  }
}
