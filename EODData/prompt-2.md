I want to incorporate ta-lib into this code and read the previously created JSON files and process each with ta-lib. 


The task is to:
1. Read the previously generated JSON files, price and volume data, and use them to make calls to ta-lib. "E:\Working\Prototypes\EODData\output"
2. Working examples of calls are in this file. "E:\Working\Prototypes\EODData\talib-scratch.py"
3. These examples are just that: quick and dirty examples. Feel free to change them to something that makes more sense if you envision it. 
4. Write out the results from each ta-lib call per ticker to a CSV file. "E:\Working\Prototypes\EODData\output\ta-lib.csv"
5. Write Python output to the Python directory. "E:\Working\Prototypes\EODData\python"

I work with take the CSV output for in Excel and do additional analysis.

As I find something that could be done in the Python code, I will let you know. We can then update the Python code 
to do some analysis before I get it  to Excel. 

There are 491 JSON files in the output directory, so there should be 491 lines in the CSV file. 
Only the last value of the calculation goes in the CSV file column. For example, the SMA will have a lot of values, but only I want the last one 
in the CSV file. Plus an additional line for the header.

Have fun. 