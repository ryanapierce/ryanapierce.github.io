import json

def process_data():
    """Reads raw stock data, processes it, and saves it as a transformed JSON file."""
    with open("/tmp/raw_data.json", "r") as f:
        data = json.load(f)
    
    # Clean and transform the data
    transformed_data = [
        {
            "symbol": item["symbol"],
            "name": item["name"].title(),  # Capitalize name
            "price": float(item["price"]),
            "market_cap": int(item["market_cap"]),
            "volume": int(item["volume"])
        }
        for item in data
    ]
    
    # Save the transformed data to a file
    with open("/tmp/transformed_data.json", "w") as f:
        json.dump(transformed_data, f)
    print("Data transformation completed.")