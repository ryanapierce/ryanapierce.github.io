import os
import json
import requests
import logging
import openai
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize Flask application
application = Flask(__name__, static_folder="static", template_folder="templates")
CORS(application)  # Enable CORS globally

# Setup rate limiter (limits each IP to 10 requests per minute)
limiter = Limiter(
    get_remote_address,
    app=application,
    default_limits=["10 per minute"],
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
        logging.critical(f"Failed to retrieve OpenAI API key: {e}")
        raise RuntimeError("Critical error: Missing OpenAI API key")

# Load API Key
openai_api_key = get_openai_api_key()
openai_client = openai.OpenAI(api_key=openai_api_key)

# Paths to data files
DATA_DIR = os.path.join(os.getcwd(), "assets", "projects", "about-me-chat-bot", "data")
LIFE_NOTES_PATH = os.path.join(DATA_DIR, "life_notes.json")
RESUME_DIR = os.path.join(DATA_DIR, "resumes")

def load_json(file_path):
    """Load a JSON file and return its contents."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        logging.error(f"Could not load {file_path}: {str(e)}")
        return {"error": f"Could not load {file_path}: {str(e)}"}

def load_resumes(directory):
    """Load all text-based resumes from a directory."""
    resumes = {}
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            if filename.endswith(".txt"):
                with open(os.path.join(directory, filename), "r", encoding="utf-8") as file:
                    resumes[filename] = file.read()
    return resumes

BACKEND_URL = "https://8y33u4e087.execute-api.us-east-1.amazonaws.com/prod/chat"
logging.info(f"Using Backend URL: {BACKEND_URL}")

@application.route("/")
def home():
    return render_template("ask_about_me.html", backend_url=BACKEND_URL)

@application.route("/api/chat", methods=["POST", "OPTIONS"])
@cross_origin()
@limiter.limit("10 per minute")
def chat():
    """Handles user input and returns chatbot response"""
    try:
        if request.method == "OPTIONS":
            response = jsonify({"message": "CORS preflight successful"})
            response.headers.add("Access-Control-Allow-Origin", "*")
            response.headers.add("Access-Control-Allow-Methods", "OPTIONS, POST")
            response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
            return response

        data = request.get_json()
        if not data or "messages" not in data or not data["messages"]:
            return jsonify({"error": "Invalid request format"}), 400

        user_input = data["messages"][0].get("content", "").strip()
        if not user_input:
            return jsonify({"error": "Empty message"}), 400

        logging.info(f"User Query: {user_input}")  

        # Load life_notes.json
        life_notes = load_json(LIFE_NOTES_PATH)
        
        # Load resume files
        resumes = load_resumes(RESUME_DIR)

        # Format the system prompt with Ryan Pierce's life notes and resumes
        system_prompt = (
            "You are a chatbot that provides responses based on Ryan Pierce's resume and life notes.\n\n"
            f"LIFE NOTES:\n{json.dumps(life_notes, indent=2)}\n\n"
            f"RESUMES:\n{json.dumps(resumes, indent=2)}"
        )

        # OpenAI API request with improved error handling
        try:
            response = openai_client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=200
            )
            chatbot_reply = response.choices[0].message.content
            logging.info(f"Chatbot Response: {chatbot_reply}")  
        except openai.APIError as e:
            logging.error(f"OpenAI API error: {e}")
            return jsonify({"error": "Chatbot service is currently unavailable due to an API error"}), 500
        except openai.AuthenticationError:
            logging.error("Invalid OpenAI API Key")
            return jsonify({"error": "Chatbot service is currently unavailable due to authentication issues"}), 500
        except openai.RateLimitError:
            logging.warning("Rate limit exceeded on OpenAI API")
            return jsonify({"error": "Rate limit exceeded. Please try again later."}), 429
        except Exception as e:
            logging.error(f"Unexpected OpenAI error: {e}")
            return jsonify({"error": "An unexpected error occurred"}), 500

        return jsonify({"response": chatbot_reply})

    except Exception as e:
        logging.error("An internal error has occurred", exc_info=True)
        return jsonify({"error": "An internal error has occurred"}), 500

if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    application.run(host="0.0.0.0", port=8080, debug=debug_mode)
