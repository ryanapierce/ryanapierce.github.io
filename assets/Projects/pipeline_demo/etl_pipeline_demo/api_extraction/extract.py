import requests
import json

def fetch_api_data(symbols):
    """Fetches stock data from the Yahoo Finance API based on user input and saves it as a JSON file."""
    base_url = "https://query1.finance.yahoo.com/v7/finance/quote?symbols="
    url = base_url + ",".join(symbols)
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        quotes = data.get("quoteResponse", {}).get("result", [])
        
        # Format the extracted data into a structured list
        formatted_data = [
            {
                "symbol": quote["symbol"],
                "name": quote.get("longName", "N/A"),
                "price": quote.get("regularMarketPrice", 0.0),
                "market_cap": quote.get("marketCap", 0),
                "volume": quote.get("regularMarketVolume", 0)
            }
            for quote in quotes
        ]
        
        # Save the formatted data to a file
        with open("/tmp/raw_data.json", "w") as f:
            json.dump(formatted_data, f)
        print("Data extracted successfully from Yahoo Finance API.")
    else:
        print("Failed to fetch data from Yahoo Finance API.")