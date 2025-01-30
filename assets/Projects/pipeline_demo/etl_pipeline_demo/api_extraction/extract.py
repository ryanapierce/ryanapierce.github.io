import requests
import json
import firebase_admin
from firebase_admin import credentials, db

# Initialize Firebase
cred = credentials.Certificate("firebase/firebase_credentials.json")  # Ensure you have this file
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://ryanapierce-etl-pipeline-demo-default-rtdb.firebaseio.com/'  # Replace with your Firebase project URL
})

def fetch_yahoo_data(symbols):
    """Fetch stock data from Yahoo Finance API."""
    base_url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols="
    url = base_url + ",".join(symbols)
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        quotes = data.get("quoteResponse", {}).get("result", [])
        
        formatted_data = {}
        for quote in quotes:
            formatted_data[quote["symbol"]] = {
                "name": quote.get("longName", "N/A"),
                "price": quote.get("regularMarketPrice", 0.0),
                "market_cap": quote.get("marketCap", 0),
                "volume": quote.get("regularMarketVolume", 0),
                "timestamp": quote.get("regularMarketTime", "N/A")
            }
        return formatted_data
    else:
        print("Failed to fetch data from Yahoo Finance API.")
        return {}

def load_data_to_firebase(symbols):
    """Load stock data into Firebase Realtime Database."""
    stock_data = fetch_yahoo_data(symbols)
    if stock_data:
        ref = db.reference("/stocks")  # Firebase root reference
        ref.update(stock_data)
        print("Data successfully loaded to Firebase.")
    else:
        print("No data to load into Firebase.")

if __name__ == "__main__":
    stock_symbols = ["AAPL", "GOOGL", "MSFT"]  # Add more symbols as needed
    load_data_to_firebase(stock_symbols)