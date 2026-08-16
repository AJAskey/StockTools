import csv
import json
import os
import re
import sys
import time
from datetime import datetime, timedelta
import requests

API_TOKEN = "xNrqzn9LHldoTDrvin683LoM"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "data", "stocks.csv")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

EXCHANGE_MAPPING = {
    "NASD": "NASDAQ",
    "OTCMKT": "OTCBB"
}

def sanitize_filename(symbol: str) -> str:
    """Sanitize symbol string for use as a filename on Windows."""
    return re.sub(r'[/\\?%*:|"<>]', '_', symbol)

def fetch_quotes_with_retry(exchange: str, symbol: str, start_str: str, end_str: str, max_retries: int = 5):
    """Fetch quote data from EODData API with retry logic for rate limits and transient errors."""
    mapped_exchange = EXCHANGE_MAPPING.get(exchange.upper(), exchange.upper())
    # EODData API uses '.' instead of '/' in symbols (e.g. BRK.B for BRK/B)
    api_symbol = symbol.replace("/", ".")
    url = f"https://api.eoddata.com/Quote/List/{mapped_exchange}/{api_symbol}?ApiKey={API_TOKEN}&Interval=d&FromDateStamp={start_str}&ToDateStamp={end_str}"
    
    backoff = 1.0
    for attempt in range(1, max_retries + 1):
        try:
            response = requests.get(url, timeout=15)
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict) and "Message" in data:
                    print(f"[{symbol}] API message: {data['Message']}", flush=True)
                    return []
                return []
            elif response.status_code == 404:
                print(f"[{symbol}] HTTP 404 Not Found.", flush=True)
                return None
            elif response.status_code == 429:
                print(f"[{symbol}] Rate limited (429). Retrying in {backoff:.1f}s (Attempt {attempt}/{max_retries})...", flush=True)
                time.sleep(backoff)
                backoff *= 2.0
            else:
                print(f"[{symbol}] HTTP {response.status_code} response. Retrying in {backoff:.1f}s...", flush=True)
                time.sleep(backoff)
                backoff *= 1.5
        except requests.exceptions.RequestException as e:
            print(f"[{symbol}] Network error: {e}. Retrying in {backoff:.1f}s...", flush=True)
            time.sleep(backoff)
            backoff *= 1.5
            
    print(f"[{symbol}] Failed after {max_retries} attempts.", flush=True)
    return None

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    end_date = datetime.now()
    # 370 calendar days will cover ~250 trading days including weekends and holidays
    start_date = end_date - timedelta(days=370)
    end_str = end_date.strftime("%Y-%m-%d")
    start_str = start_date.strftime("%Y-%m-%d")
    
    print(f"Reading tickers from: {CSV_PATH}", flush=True)
    if not os.path.exists(CSV_PATH):
        print(f"Error: {CSV_PATH} not found!", flush=True)
        sys.exit(1)
        
    stocks = []
    with open(CSV_PATH, "r", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for row in reader:
            stocks.append(row)
            
    total_stocks = len(stocks)
    print(f"Found {total_stocks} stocks to process.", flush=True)
    print(f"Downloading historical data (last 250 trading days)...", flush=True)
    print(f"Date range query: {start_str} to {end_str}", flush=True)
    
    successful = 0
    failed = 0
    
    for idx, stock in enumerate(stocks, 1):
        symbol = stock.get("Symbol", "").strip()
        name = stock.get("Name", "").strip()
        exchange = stock.get("Exchange", "").strip()
        sector = stock.get("Sector", "").strip()
        industry = stock.get("Industry", "").strip()
        
        if not symbol:
            continue
            
        filename = f"{sanitize_filename(symbol)}.json"
        out_filepath = os.path.join(OUTPUT_DIR, filename)
        
        # Check if already downloaded and valid
        if os.path.exists(out_filepath):
            try:
                with open(out_filepath, "r", encoding="utf-8") as existing_f:
                    existing_data = json.load(existing_f)
                    if existing_data.get("data_count", 0) >= 200:
                        successful += 1
                        if idx % 50 == 0 or idx == total_stocks:
                            print(f"Progress: [{idx}/{total_stocks}] - Already downloaded {symbol} ({existing_data.get('data_count')} quotes). Total Success: {successful}, Failed: {failed}", flush=True)
                        continue
            except Exception:
                pass
        
        quotes = fetch_quotes_with_retry(exchange, symbol, start_str, end_str)
        
        if quotes is not None:
            # Sort quotes by dateStamp ascending if needed
            quotes.sort(key=lambda x: x.get("dateStamp", ""))
            # Keep the last 250 trading days
            quotes_250 = quotes[-250:] if len(quotes) > 250 else quotes
            
            output_data = {
                "symbol": symbol,
                "name": name,
                "exchange": exchange,
                "sector": sector,
                "industry": industry,
                "data_count": len(quotes_250),
                "data": quotes_250
            }
            
            with open(out_filepath, "w", encoding="utf-8") as out_f:
                json.dump(output_data, out_f, indent=2)
                
            successful += 1
            if idx % 25 == 0 or idx == total_stocks:
                print(f"Progress: [{idx}/{total_stocks}] - Successfully processed {symbol} ({len(quotes_250)} quotes saved). Total Success: {successful}, Failed: {failed}", flush=True)
        else:
            failed += 1
            print(f"Progress: [{idx}/{total_stocks}] - FAILED to fetch data for {symbol}.", flush=True)
            
        # Pacing delay to respect API rate limits
        time.sleep(0.2)
        
    print("\n--- Download Complete ---", flush=True)
    print(f"Total Tickers Processed: {total_stocks}", flush=True)
    print(f"Successfully Saved: {successful}", flush=True)
    print(f"Failed: {failed}", flush=True)
    print(f"Output files saved in: {OUTPUT_DIR}", flush=True)

if __name__ == "__main__":
    main()
