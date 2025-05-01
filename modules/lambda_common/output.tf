output "lambda_layer_common_arn" {
  value = aws_lambda_layer_version.common.arn
}

output "sns_topic_arn" {
  value = aws_sns_topic.main.arn
}
