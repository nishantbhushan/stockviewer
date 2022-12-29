import yfinance 
from datetime import date
import pandas as pd

def stockChart(tickerName, rangeOption, startDate):

    stockData= {}
    tickerData=yfinance.Ticker(tickerName)

    end_date = date.today()
    if startDate is None:
        startDate=date(end_date.year -5,1,1)
    start_date = startDate.strftime('%Y-%m-%d')
    end_date = end_date.strftime('%Y-%m-%d')

    if rangeOption=='1D':        
        tickerData = tickerData.history(interval='1h',start=start_date,end=end_date)
        min_price = tickerData.head(1)['Close'].iloc[0]
        max_price = tickerData.tail(1)['Close'].iloc[0]
    else:
        tickerData = tickerData.history(start=start_date,end=end_date)
        min_price = tickerData.head(1)['Close'].iloc[0]
        max_price = tickerData.tail(1)['Close'].iloc[0]
    
    tickerData=tickerData.reset_index().rename(columns={'index':'Date'})[['Date','Close']].to_dict('records')

    stockData['tickerData'] = tickerData
    stockData['min_price'] = min_price
    stockData['max_price'] = max_price


    return stockData

