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
AWS_REGION = "us-east-1"  # Change to your region
SECRET_NAME = "OPENAI_API_KEY"  # Change to the name of your secret

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

@application.route("/chat", methods=["POST"])
def chat():
    """Handles user input and returns chatbot response"""
    try:
        user_input = request.json.get("message", "").strip()
        if not user_input:
            logging.warning("Received empty user message.")
            return jsonify({"error": "Empty message"}), 400

        logging.info(f"User Input: {user_input}")

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
        logging.info(f"Chatbot Response: {chatbot_reply}")

        return jsonify({"response": chatbot_reply})

    except Exception as e:
        logging.error(f"Chatbot API Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    application.run(host="0.0.0.0", port=5000)
