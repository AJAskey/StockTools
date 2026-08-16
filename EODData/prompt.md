I got a simple little program to build today, mostly to test out my environment but also to give you something to do. I need to access my EODData account. Pull down ticker data for all the symbols in data/stocks.csv and write The downloaded price and volume data into JSON files. 

The file "E:\Working\Prototypes\EODData\data\stocks.csv" has this format : 

Symbol,Name,Exchange,Sector,Industry
A,Agilent Technologies, Inc.,NYSE,Health Care,Medical Equipment
AA,Alcoa Corp.,NYSE,Materials,Aluminum

The symbol and the exchange will be needed to make the call to EOD data. I have working prototypes of a simple tests of this in files eodapi-scratch.py and eod-scratch2.py.

My personal API token for EOD data is API_TOKEN = "".

The EOD data specification document is in this JSON file : "E:\Working\Prototypes\EODData\Specs\eoddata-spec.json"
Additional EODData information is found in this file "E:\Working\Prototypes\EODData\Specs\EODData.md"

The task is to:
1. Ingest every ticker symbol from stocks.csv.
2. Create a call to eoddata.
3. Download the last 250 days of data.
4. Write out each ticker separately in its own JSON file. Example: AA.json
5. Add the industry and sector to that JSON file also. 
6. Write the data files to this directory: "E:\Working\Prototypes\EODData\output"

The use for these JSON files will be read in later by a different program to plot the data. 

Write Python output to the Python directory. "E:\Working\Prototypes\EODData\python"
