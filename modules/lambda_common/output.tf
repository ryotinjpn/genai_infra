output "lambda_layer_arn" {
  value = aws_lambda_layer_version.main.arn
}

output "sns_topic_arn" {
  value = aws_sns_topic.main.arn
}
