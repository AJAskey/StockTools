import csv
import logging
import os
import pandas as pd

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("process_options_flow")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "output")

OPTIONS_FLOW_PATH = os.path.join(DATA_DIR, "options_flow_stock.csv")
STOCKS_PATH = os.path.join(DATA_DIR, "stocks.csv")

STOCK_FLOW_PATH = os.path.join(OUTPUT_DIR, "option_stock_flow.csv")
INDUSTRY_FLOW_PATH = os.path.join(OUTPUT_DIR, "option_industry_flow.csv")
SECTOR_FLOW_PATH = os.path.join(OUTPUT_DIR, "option_sector_flow.csv")


def clean_total_value(val):
    """Clean string formatted numbers into float amounts."""
    if pd.isna(val):
        return 0.0
    val_str = str(val).replace(",", "").replace('"', "").strip()
    try:
        return float(val_str)
    except ValueError:
        logger.warning(f"Could not convert total_value '{val}' to float. Defaulting to 0.0")
        return 0.0


def main():
    logger.info("Starting options flow data processing...")
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 1. Read input files
    if not os.path.exists(OPTIONS_FLOW_PATH):
        logger.error(f"Options flow file not found: {OPTIONS_FLOW_PATH}")
        return
    if not os.path.exists(STOCKS_PATH):
        logger.error(f"Stocks file not found: {STOCKS_PATH}")
        return

    df_flow = pd.read_csv(OPTIONS_FLOW_PATH)
    df_stocks = pd.read_csv(STOCKS_PATH)

    logger.info(f"Loaded {len(df_flow)} records from options_flow_stock.csv")
    logger.info(f"Loaded {len(df_stocks)} records from stocks.csv")

    # 2. Build stock lookup dictionary: Symbol -> (Industry, Sector)
    stock_lookup = {}
    for idx, row in df_stocks.iterrows():
        symbol = str(row["Symbol"]).strip() if pd.notna(row["Symbol"]) else ""
        industry = str(row["Industry"]).strip() if pd.notna(row["Industry"]) else ""
        sector = str(row["Sector"]).strip() if pd.notna(row["Sector"]) else ""
        if symbol:
            stock_lookup[symbol] = {"Industry": industry, "Sector": sector}

    # Clean flow data
    df_flow["clean_ticker"] = df_flow["ticker"].astype(str).str.strip()
    df_flow["clean_sentiment"] = df_flow["sentiment"].astype(str).str.strip().str.lower()
    df_flow["clean_option_type"] = df_flow["option_type"].astype(str).str.strip().str.upper()
    df_flow["clean_total_value"] = df_flow["total_value"].apply(clean_total_value)

    # Map Industry and Sector, log warning for missing tickers
    matched_industries = []
    matched_sectors = []
    unmatched_tickers = set()

    for ticker in df_flow["clean_ticker"]:
        if ticker in stock_lookup:
            matched_industries.append(stock_lookup[ticker]["Industry"])
            matched_sectors.append(stock_lookup[ticker]["Sector"])
        else:
            matched_industries.append(None)
            matched_sectors.append(None)
            unmatched_tickers.add(ticker)

    df_flow["Industry"] = matched_industries
    df_flow["Sector"] = matched_sectors

    if unmatched_tickers:
        logger.warning(
            f"Found {len(unmatched_tickers)} ticker(s) in options flow not matched in stocks.csv:"
        )
        for ticker in sorted(unmatched_tickers):
            logger.warning(f"  - Ticker '{ticker}' not found in stocks.csv")

    # Categories definition
    categories = [
        ("CALL", "bullish"),
        ("CALL", "neutral"),
        ("CALL", "bearish"),
        ("PUT", "bullish"),
        ("PUT", "neutral"),
        ("PUT", "bearish"),
    ]

    def build_flow_table(group_col, index_label):
        """Aggregate total_value by group_col and build output dataframe."""
        grouped_data = {}

        # Exclude NaN/None group keys
        valid_df = df_flow.dropna(subset=[group_col])

        for _, row in valid_df.iterrows():
            key = row[group_col]
            if not key or pd.isna(key):
                continue

            if key not in grouped_data:
                grouped_data[key] = {cat: 0.0 for cat in categories}

            opt_type = row["clean_option_type"]
            sentiment = row["clean_sentiment"]
            val = row["clean_total_value"]

            cat_key = (opt_type, sentiment)
            if cat_key in grouped_data[key]:
                grouped_data[key][cat_key] += val

        sorted_keys = sorted(grouped_data.keys())

        # Construct CSV rows with 2 header rows
        # Row 1: index_label, CALL, CALL, CALL, PUT, PUT, PUT
        # Row 2: index_label, Bullish, Neutral, Bearish, Bullish, Neutral, Bearish
        header_row1 = [index_label, "CALL", "CALL", "CALL", "PUT", "PUT", "PUT"]
        header_row2 = [index_label, "Bullish", "Neutral", "Bearish", "Bullish", "Neutral", "Bearish"]

        rows = [header_row1, header_row2]

        for key in sorted_keys:
            row_vals = [key]
            for cat in categories:
                row_vals.append(grouped_data[key][cat])
            rows.append(row_vals)

        return rows

    def build_stock_flow_table():
        """Aggregate total_value by ticker and include Industry and Sector metadata columns."""
        grouped_data = {}

        valid_df = df_flow.dropna(subset=["clean_ticker"])

        for _, row in valid_df.iterrows():
            key = row["clean_ticker"]
            if not key or pd.isna(key):
                continue

            if key not in grouped_data:
                grouped_data[key] = {cat: 0.0 for cat in categories}

            opt_type = row["clean_option_type"]
            sentiment = row["clean_sentiment"]
            val = row["clean_total_value"]

            cat_key = (opt_type, sentiment)
            if cat_key in grouped_data[key]:
                grouped_data[key][cat_key] += val

        sorted_keys = sorted(grouped_data.keys())

        header_row1 = ["Ticker", "Industry", "Sector", "CALL", "CALL", "CALL", "PUT", "PUT", "PUT"]
        header_row2 = ["Ticker", "Industry", "Sector", "Bullish", "Neutral", "Bearish", "Bullish", "Neutral", "Bearish"]

        rows = [header_row1, header_row2]

        for key in sorted_keys:
            stock_info = stock_lookup.get(key, {})
            ind = stock_info.get("Industry", "")
            sec = stock_info.get("Sector", "")
            row_vals = [key, ind, sec]
            for cat in categories:
                row_vals.append(grouped_data[key][cat])
            rows.append(row_vals)

        return rows

    def write_csv(filepath, rows):
        try:
            with open(filepath, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(rows)
            logger.info(f"Successfully generated: {filepath} ({len(rows) - 2} data rows)")
        except PermissionError:
            logger.error(
                f"Permission denied when writing to '{filepath}'. "
                "Please close the file if it is open in Excel or another application and try again."
            )


    # Generate Stock Flow Table (with Industry & Sector columns)
    stock_rows = build_stock_flow_table()
    write_csv(STOCK_FLOW_PATH, stock_rows)

    # Generate Industry Flow Table
    industry_rows = build_flow_table("Industry", "Industry")
    write_csv(INDUSTRY_FLOW_PATH, industry_rows)

    # Generate Sector Flow Table
    sector_rows = build_flow_table("Sector", "Sector")
    write_csv(SECTOR_FLOW_PATH, sector_rows)

    logger.info("Options flow data processing completed successfully.")


if __name__ == "__main__":
    main()

