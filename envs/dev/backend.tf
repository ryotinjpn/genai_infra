terraform {
  backend "s3" {
    bucket       = "tfstate-genai-dev-ap-northeast-1"
    key          = "terrafrom-playground.tfstate"
    region       = "ap-northeast-1"
    encrypt      = true
    use_lockfile = true
  }
}
