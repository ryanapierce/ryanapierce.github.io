resource "aws_secretsmanager_secret" "openai_api_key" {
  name = "OpenAIAPIKey"
}

resource "aws_secretsmanager_secret_version" "openai_api_key" {
  secret_id     = aws_secretsmanager_secret.openai_api_key.id
  secret_string = "your-openai-api-key"  # Replace with your actual API key
}
