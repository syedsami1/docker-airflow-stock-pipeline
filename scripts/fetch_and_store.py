import os
import json
import psycopg2
import requests

# Get environment variables from Docker / Airflow
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")
DB_USER = os.getenv("POSTGRES_USER", "airflow")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD", "airflow")
DB_NAME = os.getenv("POSTGRES_DB", "stocks_db")
DB_HOST = os.getenv("POSTGRES_HOST", "postgres")  # default hostname in docker-compose

STOCK_SYMBOL = "AAPL"
API_URL = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={STOCK_SYMBOL}&apikey={API_KEY}"


def fetch_stock_data():
    """
    Fetch the latest daily stock data for the given symbol from Alpha Vantage API.
    """
    try:
        response = requests.get(API_URL)
        response.raise_for_status()
        data = response.json()

        if "Time Series (Daily)" not in data:
            raise ValueError(f"API returned invalid data: {data}")

        latest_date = list(data["Time Series (Daily)"].keys())[0]
        daily_data = data["Time Series (Daily)"][latest_date]

        return {
            "date": latest_date,
            "open": float(daily_data["1. open"]),
            "high": float(daily_data["2. high"]),
            "low": float(daily_data["3. low"]),
            "close": float(daily_data["4. close"]),
            "volume": int(daily_data["5. volume"]),
        }

    except Exception as e:
        print(f"[ERROR] Failed to fetch stock data: {e}")
        return None


def store_to_db(stock_data):
    """
    Store the stock data into Postgres database.
    Creates the table if it does not exist.
    """
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS stock_prices (
                date DATE PRIMARY KEY,
                open FLOAT,
                high FLOAT,
                low FLOAT,
                close FLOAT,
                volume BIGINT
            );
        """)

        cursor.execute("""
            INSERT INTO stock_prices (date, open, high, low, close, volume)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (date) DO UPDATE SET
                open = EXCLUDED.open,
                high = EXCLUDED.high,
                low = EXCLUDED.low,
                close = EXCLUDED.close,
                volume = EXCLUDED.volume;
        """, (
            stock_data["date"],
            stock_data["open"],
            stock_data["high"],
            stock_data["low"],
            stock_data["close"],
            stock_data["volume"],
        ))

        conn.commit()
        cursor.close()
        conn.close()

        print(f"[INFO] Successfully stored data for {stock_data['date']}")

    except Exception as e:
        print(f"[ERROR] Database operation failed: {e}")


if __name__ == "__main__":
    data = fetch_stock_data()
    if data:
        store_to_db(data)
    else:
        print("[WARN] No data to store.")
