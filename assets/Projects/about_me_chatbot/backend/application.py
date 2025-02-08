from flask import Flask, request, jsonify
import requests
import json
import openai
import os
import logging
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from flask_cors import CORS

# Initialize Flask app
application = Flask(__name__)
CORS(application)

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("chatbot.log"), logging.StreamHandler()]
)

# AWS Secrets Manager configuration
AWS_REGION = "us-east-1"  # Change to your AWS region
SECRET_NAME = "OPENAI_API_KEY"  # Change to the actual secret name

def get_openai_api_key():
    """Fetch OpenAI API key from AWS Secrets Manager"""
    try:
        session = boto3.session.Session()
        client = session.client(service_name="secretsmanager", region_name=AWS_REGION)
        secret_value = client.get_secret_value(SecretId=SECRET_NAME)
        return json.loads(secret_value["SecretString"])["OPENAI_API_KEY"]
    except NoCredentialsError:
        logging.error("AWS credentials not found.")
        return None
    except PartialCredentialsError:
        logging.error("Incomplete AWS credentials.")
        return None
    except Exception as e:
        logging.error(f"Error fetching secret: {str(e)}")
        return None

# Load API Key
openai.api_key = get_openai_api_key()
if not openai.api_key:
    logging.error("OpenAI API key could not be retrieved.")

@application.route("/api/chat", methods=["POST"])
def chat():
    """Handles user input and returns chatbot response"""
    try:
        data = request.get_json()

        # Validate request payload
        if not data or "messages" not in data or not data["messages"]:
            logging.warning(f"Invalid request received: {data}")
            return jsonify({"error": "Invalid request format"}), 400

        user_input = data["messages"][0].get("content", "").strip()
        if not user_input:
            logging.warning("Received empty user message.")
            return jsonify({"error": "Empty message"}), 400

        user_ip = request.remote_addr
        logging.info(f"User [{user_ip}] Input: {user_input}")

        # OpenAI API request
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a chatbot that provides responses based on Ryan Pierce's resume and life notes."},
                {"role": "user", "content": user_input}
            ],
            max_tokens=200
        )

        chatbot_reply = response["choices"][0]["message"]["content"]
        logging.info(f"User [{user_ip}] Chatbot Response: {chatbot_reply}")

        return jsonify({"response": chatbot_reply})

    except openai.error.OpenAIError as e:
        logging.error(f"OpenAI API Error: {str(e)}")
        return jsonify({"error": "Chatbot service is currently unavailable"}), 500

    except Exception as e:
        logging.error(f"Unexpected Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=8080)