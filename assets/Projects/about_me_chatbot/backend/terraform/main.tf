provider "aws" {
  region = "us-east-1"
}

# Create an S3 bucket for Elastic Beanstalk deployments
resource "aws_s3_bucket" "eb_bucket" {
  bucket = "about-me-chatbot-eb"
  force_destroy = true
}

# IAM Role for Elastic Beanstalk
resource "aws_iam_role" "eb_role" {
  name = "about-me-chatbot-eb-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = { Service = "elasticbeanstalk.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "eb_role_policy" {
  role       = aws_iam_role.eb_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

# Elastic Beanstalk Application
resource "aws_elastic_beanstalk_application" "chatbot_app" {
  name = "about-me-chatbot"
}

# Elastic Beanstalk Environment
resource "aws_elastic_beanstalk_environment" "chatbot_env" {
  name                = "about-me-chatbot-env"
  application         = aws_elastic_beanstalk_application.chatbot_app.name
  solution_stack_name = "64bit Amazon Linux 2 v5.8.0 running Python 3.8"

  setting {
    namespace = "aws:elasticbeanstalk:environment"
    name      = "EnvironmentType"
    value     = "SingleInstance"
  }

  setting {
    namespace = "aws:elasticbeanstalk:application:environment"
    name      = "OPENAI_API_KEY"
    value     = aws_secretsmanager_secret_version.openai_api_key.secret_string
  }
}