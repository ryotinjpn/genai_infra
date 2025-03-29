# -------------------------------------
# DynamoDB
# -------------------------------------
resource "aws_dynamodb_table" "generate_post_to_x" {
  name           = "GeneratePostToXHistory"
  billing_mode   = "PAY_PER_REQUEST"
  read_capacity  = 1
  write_capacity = 1
  hash_key       = "HistoryId"

  attribute {
    name = "HistoryId"
    type = "S"
  }

  ttl {
    attribute_name = "ExpireAt"
    enabled        = true
  }
}
