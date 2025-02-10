import boto3
import json

AWS_REGION = "us-east-1"
SECRET_NAME = "OPENAI_API_KEY"

session = boto3.session.Session()
client = session.client(service_name="secretsmanager", region_name=AWS_REGION)

try:
    secret_value = client.get_secret_value(SecretId=SECRET_NAME)
    print(json.loads(secret_value["SecretString"])["OPENAI_API_KEY"])
except Exception as e:
    print(f"Error fetching secret: {str(e)}")
