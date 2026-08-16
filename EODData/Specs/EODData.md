# EODData API

v1

OAS 3.0.1

# EODData API

Download OpenAPI Document

json

Download OpenAPI Document

yaml

Modern API that provides access to historical market data from a selection of leading global exchanges. To get started you will need to [REGISTER](https://eoddata.com/register.aspx) for an account and authenticate your requests. Using our API you can download quotes, dividends, fundamentals, technical indicators, splits, and much more.  
  

#### Authentication

Simply append 'apiKey=\[yourApiKey\]' to all of your requests.  
Get your ApiKey from [HERE](https://eoddata.com/myaccount/api.aspx "Get your ApiKey")

Server

Server:https://api.eoddata.com

Client Libraries

Shell

Ruby

Node.js

PHP

Python

More Select from all clients

Python http.client

## Customer

​Copy link

Includes the ability to Login using your credentials and gain a bearer token that can be included in your request headers to authenticate your requests.

## Exchanges (Collapsed)

​Copy link

Download the list of available Exchanges or retrieve specific information for a given Exchange. All of our data is segregated by Exchange, for example 'NASDAQ' Exchange information includes code, name, currency, timezone, country, etc

Exchanges Operations

-   get/Exchange/List
-   get/Exchange/Get/{exchangeCode}

Show More

## Symbols (Collapsed)

​Copy link

API Methods for downloading lists of available Symbols for each Exchange or retrieve specific information for a given Symbol.

Symbols Operations

-   get/Symbol/List/{exchangeCode}
-   get/Symbol/Get/{exchangeCode}/{symbolCode}
-   get/Symbol/Search/{searchString}

Show More

## Quotes (Collapsed)

​Copy link

Returns current and 30+ years of historical data in OHLCV (Open, High, Low, Close, Volume, \[OpenInterest\]) format. A full range of time intervals is available: 1min, 5min, 10min, 15min, 30min, Hourly, Daily, Weekly, Monthly, Quarterly, Yearly

Quotes Operations

-   get/Quote/List/{exchangeCode}
-   get/Quote/Get/{exchangeCode}/{symbolCode}
-   get/Quote/List/{exchangeCode}/{symbolCode}

Show More

## Corporate (Collapsed)

​Copy link

More detailed information about each symbol including: description, address, FIGI, CUSIP, ISIN, etc. Corporate actions: Splits and Dividends.

Corporate Operations

-   get/Profile/List/{exchangeCode}
-   get/Profile/Get/{exchangeCode}/{symbolCode}
-   get/Splits/List/{exchangeCode}
-   get/Splits/List/{exchangeCode}/{symbolCode}
-   get/Dividends/List/{exchangeCode}
-   get/Dividends/List/{exchangeCode}/{symbolCode}

Show More

## Fundamental Data (Collapsed)

​Copy link

This group of endpoints provide Fundamental Data such as PE, EPS, Dividend Yield, Market Capitalization, Shares Outstanding and much more.

Fundamental Data Operations

-   get/Fundamental/List/{exchangeCode}
-   get/Fundamental/Get/{exchangeCode}/{symbolCode}

Show More

## Technical Data

​Copy link

Endpoints which return our pre-built selection of technical indicators that include: MA5, MA20, STO9, RSI14, WPR14, MTM14, etc

## Metadata (Collapsed)

​Copy link

All Metadata related operations

Metadata Operations

-   get/ExchangeType/List
-   get/SymbolType/List
-   get/Country/List
-   get/Currency/List

Show More

## Technical Indicators

​Copy link

Technical Indicators Operations

-   get/Technical/List/{exchangeCode}
-   get/Technical/Get/{exchangeCode}/{symbolCode}

### Technical List

​Copy link

Returns a list of Technical Indicators for a given Exchange

Path Parameters

-   exchangeCodeCopy link to exchangeCode
    
    Type: string
    
    required
    

Query Parameters

-   ApiKeyCopy link to ApiKey
    
    Type: string
    
    required
    

Responses

-   200
    
    OK
    
    application/json
    
-   401Copy link to 401
    
    Unauthorized
    
-   404Copy link to 404
    
    Not Found
    
-   429Copy link to 429
    
    Too Many Requests
    

Request Example for get/Technical/List/_{exchangeCode}_

Python http.client

```python
import http.client

conn = http.client.HTTPSConnection("api.eoddata.com")

conn.request("GET", "/Technical/List/%7BexchangeCode%7D")

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
```

Test Request(get /Technical/List/{exchangeCode})

Status: 200Status: 401Status: 404Status: 429

Show Schema 

```json
[
  {
    "exchangeCode": "string",
    "symbolCode": "string",
    "quarterChange": 1,
    "biannualChange": 1,
    "ytdChange": 1,
    "weekLow": 1,
    "weekHigh": 1,
    "weekChange": 1,
    "weekVolume": 1,
    "weekAvgVolume": 1,
    "weekAvgChange": 1,
    "weekYield": 1,
    "monthLow": 1,
    "monthHigh": 1,
    "monthChange": 1,
    "monthVolume": 1,
    "monthAvgVolume": 1,
    "monthAvgChange": 1,
    "monthYield": 1,
    "yearLow": 1,
    "yearHigh": 1,
    "yearChange": 1,
    "yearVolume": 1,
    "yearAvgVolume": 1,
    "yearAvgChange": 1,
    "yearYield": 1,
    "mA5": 1,
    "mA10": 1,
    "mA20": 1,
    "mA50": 1,
    "mA100": 1,
    "mA200": 1,
    "wmA5": 1,
    "wmA10": 1,
    "wmA20": 1,
    "wmA50": 1,
    "wmA100": 1,
    "wmA200": 1,
    "emA5": 1,
    "emA10": 1,
    "emA20": 1,
    "emA50": 1,
    "emA100": 1,
    "emA200": 1,
    "macd": 1,
    "stO9Fast": 1,
    "stO9Slow": 1,
    "stO9Full": 1,
    "stO14Fast": 1,
    "stO14Slow": 1,
    "stO14Full": 1,
    "rsI9": 1,
    "rsI14": 1,
    "wpR14": 1,
    "mtM14": 1,
    "roC14": 1,
    "upperBB20": 1,
    "lowerBB20": 1,
    "bandwidthBB20": 1,
    "obV20": 1,
    "aD20": 1,
    "aroon20": 1,
    "dmiPositive": 1,
    "dmiNegative": 1,
    "dmiAverage": 1,
    "atr": 1,
    "cci": 1,
    "sar": 1,
    "volatility": 1,
    "liquidity": 1
  }
]
```

OK

### Technical Get

​Copy link

Return Technical data for a given Exchange and Symbol

Path Parameters

-   exchangeCodeCopy link to exchangeCode
    
    Type: string
    
    required
    
-   symbolCodeCopy link to symbolCode
    
    Type: string
    
    required
    

Query Parameters

-   ApiKeyCopy link to ApiKey
    
    Type: string
    
    required
    

Responses

-   200
    
    OK
    
    application/json
    
-   401Copy link to 401
    
    Unauthorized
    
-   404Copy link to 404
    
    Not Found
    
-   429Copy link to 429
    
    Too Many Requests
    

Request Example for get/Technical/Get/_{exchangeCode}_/_{symbolCode}_

Python http.client

```python
import http.client

conn = http.client.HTTPSConnection("api.eoddata.com")

conn.request("GET", "/Technical/Get/%7BexchangeCode%7D/%7BsymbolCode%7D")

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
```

Test Request(get /Technical/Get/{exchangeCode}/{symbolCode})

Status: 200Status: 401Status: 404Status: 429

Show Schema 

```json
{
  "exchangeCode": "string",
  "symbolCode": "string",
  "quarterChange": 1,
  "biannualChange": 1,
  "ytdChange": 1,
  "weekLow": 1,
  "weekHigh": 1,
  "weekChange": 1,
  "weekVolume": 1,
  "weekAvgVolume": 1,
  "weekAvgChange": 1,
  "weekYield": 1,
  "monthLow": 1,
  "monthHigh": 1,
  "monthChange": 1,
  "monthVolume": 1,
  "monthAvgVolume": 1,
  "monthAvgChange": 1,
  "monthYield": 1,
  "yearLow": 1,
  "yearHigh": 1,
  "yearChange": 1,
  "yearVolume": 1,
  "yearAvgVolume": 1,
  "yearAvgChange": 1,
  "yearYield": 1,
  "mA5": 1,
  "mA10": 1,
  "mA20": 1,
  "mA50": 1,
  "mA100": 1,
  "mA200": 1,
  "wmA5": 1,
  "wmA10": 1,
  "wmA20": 1,
  "wmA50": 1,
  "wmA100": 1,
  "wmA200": 1,
  "emA5": 1,
  "emA10": 1,
  "emA20": 1,
  "emA50": 1,
  "emA100": 1,
  "emA200": 1,
  "macd": 1,
  "stO9Fast": 1,
  "stO9Slow": 1,
  "stO9Full": 1,
  "stO14Fast": 1,
  "stO14Slow": 1,
  "stO14Full": 1,
  "rsI9": 1,
  "rsI14": 1,
  "wpR14": 1,
  "mtM14": 1,
  "roC14": 1,
  "upperBB20": 1,
  "lowerBB20": 1,
  "bandwidthBB20": 1,
  "obV20": 1,
  "aD20": 1,
  "aroon20": 1,
  "dmiPositive": 1,
  "dmiNegative": 1,
  "dmiAverage": 1,
  "atr": 1,
  "cci": 1,
  "sar": 1,
  "volatility": 1,
  "liquidity": 1
}
```

OK