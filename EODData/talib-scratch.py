import numpy as np
import pandas as pd
import talib

# 1. Sample Data Setup
close_prices = np.random.random(100) * 100
df = pd.DataFrame({
    'open': close_prices - 1,
    'high': close_prices + 2,
    'low': close_prices - 2,
    'close': close_prices,
    'volume': np.random.randint(1000, 5000, 100)
})

'''
Read in each JSON file and make these calls to TA-Lib. 
These are examples. If you can envision something better, do the better way. 
'''
# 2. Standard Function API (Using NumPy Arrays)
# Calculate a 14-period Relative Strength Index (RSI)
rsi = talib.RSI(close_prices, timeperiod=14)

# Calculate Bollinger Bands
upperband, middleband, lowerband = talib.BBANDS(close_prices, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)

# 3. Abstract API (Using Pandas DataFrames)
import talib.abstract as abstract

# The dataframe must contain columns lowercase named: 'open', 'high', 'low', 'close', 'volume'
macd, macdsignal, macdhist = abstract.MACD(df, fastperiod=12, slowperiod=26, signalperiod=9)

# 4. Candlestick Pattern Recognition
# Returns 100 (bullish), -100 (bearish), or 0 (no pattern)
engulfing = talib.CDLENGULFING(df['open'].values, df['high'].values, df['low'].values, df['close'].values)

# 5. Advanced Indicators
# Calculate MACD (Moving Average Convergence Divergence)
# Returns three arrays:macd, signal_line, histogram
macd, signal_line, hist = talib.MACD(close_prices, fastperiod=12, slowperiod=26, signalperiod=9)

# Calculate ADX (Average Directional Index)
# Measures trend strength (1-100). Higher = stronger trend.
adx = talib.ADX(df['high'].values, df['low'].values, df['close'].values, timeperiod=14)

# Calculate Bollinger Bands
# Returns upper, middle, and lower bands
upper, middle, lower = talib.BBANDS(close_prices, timeperiod=20, nbdevup=2, nbdevdn=2, matype=0)

sma = talib.SMA(close_prices, timeperiod=14)

std_p = talib.STDDEV(close_prices, timeperiod=5, nbdev=1)

lr_values = talib.LINEARREG(close_prices, timeperiod=5)

#  three white soldiers pattern
# 3 white soldiers is a bullish reversal pattern. It is characterized by three consecutive white candles that close higher than the previous one.
# results = talib.CDL3LINESTRIKE(open_prices, high_prices, low_prices, close_prices)


print("\n\n\n--- Results ---")
print("\nClose Prices:\n", df['close'][-10:])
print("\nHigh Prices:\n", df['high'][-10:])
print("\nLow Prices:\n", df['low'][-10:])   
print("\nOpen Prices:\n", df['open'][-10:])
print("\nVolume Prices:\n", df['volume'][-10:])
print("\nADX (Last 5 values):\n", adx[-5:])
print("\nRSI (Last 5 values):\n", rsi[-5:])
print("\nUpper Band (Last 5 values):\n", upperband[-5:])
print("\nMACD (Last 5 values):\n", macd[-5:])
print("\nEngulfing Pattern (Last 10 values):\n", engulfing[-10:])
print("\nSMA (Last 5 values):\n", sma[-5:])
print("\nSTDDEV (Last 5 values):\n", std_p[-5:])
print("\nLINEARREG (Last 5 values):\n", lr_values[-5:]  )  
   
   