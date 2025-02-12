import firebase_admin
from firebase_admin import credentials, firestore

# Load Firebase credentials
cred = credentials.Certificate("firebase_credentials.json")
firebase_admin.initialize_app(cred)

# Initialize Firestore database
db = firestore.client()
print("Firestore database connected successfully!")
