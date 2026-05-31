import json
import os

import boto3
from openai import OpenAI

S3_BUCKET = os.environ.get("S3_BUCKET", "ryan-pierce-bot-data")
LIFE_NOTES_FILE = os.environ.get("LIFE_NOTES_FILE", "life_notes.json")
RESUME_FILE = os.environ.get("RESUME_FILE", "Ryan_Pierce_Resume.txt")
AWS_REGION = os.environ.get("AWS_REGION", "us-east-1")
SECRET_NAME = os.environ.get("OPENAI_SECRET_NAME", "OPENAI_API_KEY")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
MAX_TOKENS = int(os.environ.get("OPENAI_MAX_TOKENS", "200"))

CORS_HEADERS = {
    "Access-Control-Allow-Origin": os.environ.get("ALLOWED_ORIGIN", "*"),
    "Access-Control-Allow-Methods": "OPTIONS, POST",
    "Access-Control-Allow-Headers": "Content-Type",
}

s3_client = boto3.client("s3")
_openai_client = None
_reference_data = None


def get_openai_api_key():
    """Fetch OpenAI API key from AWS Secrets Manager."""
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name=AWS_REGION)

    try:
        secret_value = client.get_secret_value(SecretId=SECRET_NAME)
        secret_string = secret_value["SecretString"]
        try:
            return json.loads(secret_string)["OPENAI_API_KEY"]
        except json.JSONDecodeError:
            return secret_string
    except Exception as e:
        print(f"ERROR: Unable to retrieve OpenAI API Key: {e}")
        return None


def get_openai_client():
    """Create the OpenAI client lazily so startup errors return clean responses."""
    global _openai_client
    if _openai_client is None:
        api_key = os.environ.get("OPENAI_API_KEY") or get_openai_api_key()
        if not api_key:
            raise RuntimeError("OpenAI API key could not be retrieved.")
        _openai_client = OpenAI(api_key=api_key)
    return _openai_client


def get_file_from_s3(file_name):
    """Retrieve file content from S3."""
    try:
        response = s3_client.get_object(Bucket=S3_BUCKET, Key=file_name)
        return response["Body"].read().decode("utf-8")
    except Exception as e:
        print(f"ERROR: Fetching {file_name} from S3 failed: {e}")
        return None


def get_reference_data():
    """Load S3 reference data once per warm Lambda container."""
    global _reference_data
    if _reference_data is None:
        life_notes = get_file_from_s3(LIFE_NOTES_FILE)
        resume_text = get_file_from_s3(RESUME_FILE)
        if not life_notes or not resume_text:
            return None
        _reference_data = {
            "life_notes": life_notes,
            "resume_text": resume_text,
        }
    return _reference_data


def response(status_code, body):
    """Return a JSON API Gateway response with consistent CORS headers."""
    return {
        "statusCode": status_code,
        "headers": CORS_HEADERS,
        "body": json.dumps(body),
    }


def parse_body(event):
    """Parse and validate a JSON request body."""
    if not event.get("body"):
        return None, "Request body is required"

    try:
        return json.loads(event["body"]), None
    except json.JSONDecodeError:
        return None, "Request body must be valid JSON"


def lambda_handler(event, context):
    """Handles API requests and logs errors."""
    http_method = event.get("httpMethod") or event.get("requestContext", {}).get("http", {}).get("method")

    if http_method == "OPTIONS":
        print("Handling CORS preflight request")
        return response(200, {"message": "CORS preflight successful"})

    if http_method != "POST":
        return response(405, {"error": "Method not allowed"})

    data, error = parse_body(event)
    if error:
        return response(400, {"error": error})

    user_input = str(data.get("query", "")).strip()
    if not user_input:
        print("WARNING: Empty or missing query received")
        return response(400, {"error": "'query' field is required"})

    reference_data = get_reference_data()
    if not reference_data:
        print("ERROR: Failed to load S3 data")
        return response(500, {"error": "Failed to load reference data from S3"})

    system_prompt = f"""
    You are a chatbot that provides insights into Ryan Pierce's professional background.
    Respond in a natural, friendly way. Use correct grammar and punctuation.
    Reference the following data but do not explicitly mention that it comes from stored files.

    Resume:
    {reference_data["resume_text"]}

    Life Notes:
    {reference_data["life_notes"]}
    """

    try:
        completion = get_openai_client().chat.completions.create(
            model=OPENAI_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_input},
            ],
            max_tokens=MAX_TOKENS,
        )
    except Exception as e:
        print(f"ERROR: OpenAI request failed: {e}")
        return response(500, {"error": "Internal Server Error"})

    chatbot_reply = completion.choices[0].message.content
    return response(200, {"response": chatbot_reply})
