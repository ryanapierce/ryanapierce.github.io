import json
import sqlite3

def load_to_db():
    """Loads the transformed data into a SQLite database."""
    conn = sqlite3.connect("etl_pipeline.db")
    cursor = conn.cursor()
    
    # Create table if it does not exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_data (
            symbol TEXT PRIMARY KEY,
            name TEXT,
            price REAL,
            market_cap INTEGER,
            volume INTEGER
        )
    """)
    
    # Read transformed data from file
    with open("/tmp/transformed_data.json", "r") as f:
        data = json.load(f)
    
    # Insert or update data in the database
    cursor.executemany("INSERT OR REPLACE INTO stock_data (symbol, name, price, market_cap, volume) VALUES (:symbol, :name, :price, :market_cap, :volume)", data)
    conn.commit()
    conn.close()
    print("Data loaded into database successfully.")
