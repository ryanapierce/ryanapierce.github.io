from flask import Flask, request, jsonify, render_template
import openai
import boto3
import json
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Initialize Flask app
application = Flask(__name__, static_folder="static", template_folder="templates")
CORS(application)

# Setup rate limiter (limits each IP to 5 requests per minute)
limiter = Limiter(
    get_remote_address,
    app=application,
    default_limits=["5 per minute"],
    storage_uri="memory://"
)

# AWS Secrets Manager configuration
AWS_REGION = "us-east-1"
SECRET_NAME = "OPENAI_API_KEY"

def get_openai_api_key():
    """Fetch OpenAI API key from AWS Secrets Manager"""
    try:
        session = boto3.session.Session()
        client = session.client(service_name="secretsmanager", region_name=AWS_REGION)
        secret_value = client.get_secret_value(SecretId=SECRET_NAME)
        return json.loads(secret_value["SecretString"])["OPENAI_API_KEY"]
    except Exception as e:
        return None

# Load API Key
openai_api_key = get_openai_api_key()
if not openai_api_key:
    raise RuntimeError("OpenAI API key could not be retrieved.")
else:
    openai_client = openai.OpenAI(api_key=openai_api_key)

# Serve Home Page
@application.route("/")
def home():
    return render_template("ask_about_me.html")  # Ensure your HTML is inside `templates/`

# Chatbot API with rate limiting
@application.route("/api/chat", methods=["POST"])
@limiter.limit("5 per minute")  # Rate limiting: Max 5 requests per minute per user
def chat():
    """Handles user input and returns chatbot response"""
    try:
        data = request.get_json()
        if not data or "messages" not in data or not data["messages"]:
            return jsonify({"error": "Invalid request format"}), 400

        user_input = data["messages"][0].get("content", "").strip()
        if not user_input:
            return jsonify({"error": "Empty message"}), 400

        # OpenAI API request
        response = openai_client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a chatbot that provides responses based on Ryan Pierce's resume and life notes."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=200
        )

        chatbot_reply = response.choices[0].message.content

        return jsonify({"response": chatbot_reply})

    except openai.OpenAIError as e:
        return jsonify({"error": "Chatbot service is currently unavailable"}), 500

    except Exception as e:
        return jsonify({"error": "An internal error has occurred"}), 500

if __name__ == "__main__":
    application.debug = True
    application.run(host="0.0.0.0", port=8080)