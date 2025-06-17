output "lambda_layer_common_arn" {
  value = aws_lambda_layer_version.common.arn
}

output "lambda_layer_gcp_arn" {
  value = aws_lambda_layer_version.gcp.arn
}

output "sns_topic_arn" {
  value = aws_sns_topic.main.arn
}
