output "bedrock_agent_id" {
  value = awscc_bedrock_agent.main.id
}

output "bedrock_agent_alias_id" {
  value = aws_bedrockagent_agent_alias.main.agent_alias_id
}
