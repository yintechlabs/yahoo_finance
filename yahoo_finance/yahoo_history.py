import requests
import datetime as dt
import numpy as np

from yahoo_cookie import getCookie

url_prefix = "https://query1.finance.yahoo.com/v7/finance/download/"
url_format = "?period1={0}&period2={1}&interval=1d&events=history&crumb={2}"
cookieData = getCookie()
cookie=cookieData['cookie']
crumb = cookieData['crumb'] 
    
def history(ticker, fromDate, uptoDate):
    params = (int(dt.datetime(*fromDate).timestamp()), int(dt.datetime(*uptoDate).timestamp()), crumb)
    url = url_prefix + ticker + url_format.format(*params)
    data = requests.get(url, cookies={'B':cookie}).text
    return [row.split(",") for row in data.split('\n') if row]
        
def series(ticker, fromDate, uptoDate, index):
    data = history(ticker, fromDate, uptoDate)
    return [item[index] for item in data]

def adjust_close(ticker, fromDate, uptoDate): 
    return [float(x) for x in series(ticker, fromDate, uptoDate, 5)[1:]]

def volume(ticker, fromDate, uptoDate): 
    return [float(x) for x in series(ticker, fromDate, uptoDate, 6)[1:]]

def returns(ticker, fromDate, uptoDate): 
    data = np.array(adjust_close(ticker, fromDate, uptoDate))
    return data[1:] / data[:-1] - 1
       
if __name__ == "__main__":
    fromDate = (2009,1,1)
    uptoDate = (2017,5,20)
    print('-------------------')
    print(history("SPY", fromDate, uptoDate))
    print('-------------------')
    print(adjust_close("SPY", fromDate, uptoDate))
    print('-------------------')
    print(volume("SPY", fromDate, uptoDate))
    print('-------------------')
    print(returns("SPY", fromDate, uptoDate))
    