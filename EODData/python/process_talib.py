import csv
import json
import os
import sys
import numpy as np
import pandas as pd
import talib

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")
JSON_DIR = os.path.join(BASE_DIR, "data", "json")
CSV_PATH = os.path.join(OUTPUT_DIR, "ta-lib.csv")

CSV_HEADERS = [
    "Symbol",
    "Name",
    "Exchange",
    "Sector",
    "Industry",
    "Date",
    "Volume",
    "Close",
    "SMA_14",
    "SMA_50",
    "SMA_200",
    "ADX_14",
    "RSI_14",
    "MACD",
    "MACD_Signal",
    "MACD_Hist",
    "BB_Upper",
    "BB_Middle",
    "BB_Lower",
    "StdDev_5",
    "LinearReg_5",
    "CDL_Engulfing",
    "CDL_3WhiteSoldiers"
]

def fmt(val, decimals=4):
    """Format numerical values cleanly for CSV export."""
    if val is None or np.isnan(val):
        return ""
    if isinstance(val, (int, np.integer)):
        return int(val)
    return round(float(val), decimals)

def process_ticker_file(filepath):
    """Reads a ticker JSON file, calculates TA-Lib indicators, and returns the latest record."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            stock_data = json.load(f)
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None

    symbol = stock_data.get("symbol", "")
    name = stock_data.get("name", "")
    exchange = stock_data.get("exchange", "")
    sector = stock_data.get("sector", "")
    industry = stock_data.get("industry", "")
    quotes = stock_data.get("data", [])

    if not quotes or len(quotes) < 5:
        print(f"[{symbol}] Insufficient quote data ({len(quotes)} quotes).")
        return None

    # Sort quotes by date Stamp ascending
    quotes.sort(key=lambda x: x.get("dateStamp", ""))

    df = pd.DataFrame(quotes)
    
    close = df["close"].values.astype(float)
    high = df["high"].values.astype(float)
    low = df["low"].values.astype(float)
    open_p = df["open"].values.astype(float)
    volume = df["volume"].values.astype(float)

    # 1. Moving Averages & Trend Indicators
    sma_14 = talib.SMA(close, timeperiod=14)
    sma_50 = talib.SMA(close, timeperiod=50) if len(close) >= 50 else np.full_like(close, np.nan)
    sma_200 = talib.SMA(close, timeperiod=200) if len(close) >= 200 else np.full_like(close, np.nan)
    adx_14 = talib.ADX(high, low, close, timeperiod=14) if len(close) >= 14 else np.full_like(close, np.nan)
    linreg_5 = talib.LINEARREG(close, timeperiod=5)

    # 2. Oscillators & Momentum Indicators
    rsi_14 = talib.RSI(close, timeperiod=14) if len(close) >= 14 else np.full_like(close, np.nan)
    macd, macd_signal, macd_hist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9) if len(close) >= 33 else (np.full_like(close, np.nan), np.full_like(close, np.nan), np.full_like(close, np.nan))

    # 3. Volatility Indicators
    bb_upper, bb_middle, bb_lower = talib.BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0) if len(close) >= 20 else (np.full_like(close, np.nan), np.full_like(close, np.nan), np.full_like(close, np.nan))
    stddev_5 = talib.STDDEV(close, timeperiod=5, nbdev=1)

    # 4. Candlestick Pattern Indicators
    cdl_engulfing = talib.CDLENGULFING(open_p, high, low, close)
    cdl_3soldiers = talib.CDL3WHITESOLDIERS(open_p, high, low, close)

    latest_date = df["dateStamp"].iloc[-1]
    latest_close = close[-1]
    latest_vol = volume[-1]

    row = {
        "Symbol": symbol,
        "Name": name,
        "Exchange": exchange,
        "Sector": sector,
        "Industry": industry,
        "Date": latest_date,
        "Volume": fmt(latest_vol, 0),
        "Close": fmt(latest_close, 2),
        "SMA_14": fmt(sma_14[-1], 2),
        "SMA_50": fmt(sma_50[-1], 2),
        "SMA_200": fmt(sma_200[-1], 2),
        "ADX_14": fmt(adx_14[-1], 2),
        "RSI_14": fmt(rsi_14[-1], 2),
        "MACD": fmt(macd[-1], 4),
        "MACD_Signal": fmt(macd_signal[-1], 4),
        "MACD_Hist": fmt(macd_hist[-1], 4),
        "BB_Upper": fmt(bb_upper[-1], 2),
        "BB_Middle": fmt(bb_middle[-1], 2),
        "BB_Lower": fmt(bb_lower[-1], 2),
        "StdDev_5": fmt(stddev_5[-1], 4),
        "LinearReg_5": fmt(linreg_5[-1], 2),
        "CDL_Engulfing": fmt(cdl_engulfing[-1], 0),
        "CDL_3WhiteSoldiers": fmt(cdl_3soldiers[-1], 0)
    }
    return row

def main():
    if not os.path.exists(OUTPUT_DIR):
        print(f"Error: Output directory '{OUTPUT_DIR}' does not exist.")
        sys.exit(1)

    json_files = [f for f in os.listdir(JSON_DIR) if f.endswith(".json")]
    json_files.sort()
    
    total_files = len(json_files)
    print(f"Found {total_files} ticker JSON files in '{OUTPUT_DIR}'.")
    print(f"Calculating TA-Lib indicators...")

    rows = []
    processed_count = 0
    
    for filename in json_files:
        filepath = os.path.join(JSON_DIR, filename)
        row = process_ticker_file(filepath)
        if row:
            rows.append(row)
            processed_count += 1

    print(f"Writing TA-Lib summary to '{CSV_PATH}'...")
    with open(CSV_PATH, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=CSV_HEADERS)
        writer.writeheader()
        writer.writerows(rows)

    print("\n--- TA-Lib Processing Complete ---")
    print(f"Total Ticker Files: {total_files}")
    print(f"Successfully Processed Rows: {processed_count}")
    print(f"Output CSV File: {CSV_PATH}")

if __name__ == "__main__":
    main()
