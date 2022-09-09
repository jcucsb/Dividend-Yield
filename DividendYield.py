import requests
from bs4 import BeautifulSoup
import json

# List of Dividend Aristocrats

DividendStocks = [
"ABM"
,"ADM"
,"ADP"
,"AFL"
,"ALB"
,"ANDE"
,"AOS"
,"APD"
,"ATO"
,"AWR"
,"BDX"
,"BEN"
,"BKH"
,"BRO"
,"CAH"
,"CAT"
,"CB"
,"CHD"
,"CINF"
,"CL"
,"CLX"
,"CNI"
,"CSL"
,"CTAS"
,"CVX"
,"DCI"
,"DOV"
,"ECL"
,"ED"
,"EMR"
,"ENB"
,"EPD"
,"ESS"
,"EXPD"
,"FRT"
,"GD"
,"GPC"
,"GWW"
,"HRL"
,"IBM"
,"ITW"
,"JKHY"
,"JNJ"
,"KMB"
,"KO"
,"LANC"
,"LECO"
,"LEG"
,"LIN"
,"LOW"
,"MCD"
,"MDT"
,"MDU"
,"MMM"
,"NDSN"
,"NEE"
,"NFG"
,"NNN"
,"NUE"
,"NWN"
,"O"
,"ORI"
,"PEP"
,"PG"
,"PH"
,"PII"
,"PPG"
,"ROP"
,"RPM"
,"RTX"
,"SHW"
,"SJM"
,"SON"
,"SPGI"
,"SWK"
,"SYK"
,"SYY"
,"TGT"
,"TR"
,"TROW"
,"UGI"
,"UVV"
,"WBA"
,"WMT"
,"WPC"
,"WTRG"
,"XOM"
,"YORW"
]

DividendData = []

# This function reads in a ticker symbol, then uses parsing to find the current Price and Dividend of the stock from the Yahoo Finance
# website. It then creates an entry into the dictionary for each symbol and calculates the Dividend Yield per stock.
# Uses fstring to read in stock symbols
def getData(symbol):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36'}
    url = f'https://finance.yahoo.com/quote/{symbol}'
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    dividend = soup.find('table', {'class': 'W(100%) M(0) Bdcl(c)'}).find_all('tr')[5].text
    print('Testing: ', symbol)
    stock = {
    'Symbol': symbol,
    'Price': soup.find('div', {'class': 'D(ib) Mend(20px)'}).find_all('fin-streamer')[0].text,
    # Daily price change
    #'change': soup.find('div', {'class': 'D(ib) Mend(20px)'}).find_all('fin-streamer')[1].text,
    'Dividend' : dividend[24:29],
    'Dividend Yield' : float(dividend[24:29]) / float(soup.find('div', {'class': 'D(ib) Mend(20px)'}).find_all('fin-streamer')[0].text)
    }
    return stock

# Appends the stocks within DividendStocks and their corresponding data to the empty Dictionary DividendData

for item in DividendStocks:
    DividendData.append(getData(item))

# This uses a lambda expression to sort the dictionary by the relevant key
# In this case I sorted by Dividend Yield since I want to find the highest Daily Dividend Yield 
# for all the Dividend Aristocrats. Sorts by greatest by adding the reverse=True parameter 


DividendData = sorted(DividendData, key = lambda x: x['Dividend Yield'], reverse=True)
print(DividendData)

Top10 = DividendData[0:10]

print("The Top 10 Dividend Stocks are: ")
for items in Top10:
    print(items, "\n")

''' Alternate method to scrape for price and change
price = soup.find('fin-streamer', {'class': 'Fw(b) Fz(36px) Mb(-4px) D(ib)'}).text
change = soup.find('fin-streamer', {'class': 'Fw(500) Pstart(8px) Fz(24px)'}).text
'''

# Dividend Data JSON file

with open('DividendData.json', 'w') as f:
    json.dump(DividendData, f)

print("DividendData JSON file created")

# Top 10 Dividend Stocks JSON file

with open('Top10Dividend.json', 'w') as f:
    json.dump(Top10, f)

print("Top10DividendStocks JSON file created")