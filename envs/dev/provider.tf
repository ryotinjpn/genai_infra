provider "aws" {
  region = "ap-northeast-1"

  default_tags {
    tags = {
      ProjectName = "genai"
      Environment = "dev"
    }
  }
}

provider "aws" {
  region = "us-east-1"
  alias  = "versinia"

  default_tags {
    tags = {
      ProjectName = "genai"
      Environment = "dev"
    }
  }
}
