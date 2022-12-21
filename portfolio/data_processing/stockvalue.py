import yfinance 
import pandas
import numpy
from datetime import datetime, timedelta


def getStockValue(stockTicker):
    # stockTickerValue = yf.Ticker(stockTicker).info['regularMarketPrice']
    # print(f"value of {stockTicker} is {stockTickerValue} !")
    df = pd.DataFrame(stockTicker)
    df['stockvalue'] = df.apply(lambda row : yfinance.Ticker(row['ticker']).info['regularMarketPrice'], axis = 1)
    df.datePurchased = pd.to_datetime(df.datePurchased)
    # print(yf.Ticker('AAPL').info['regularMarketPrice'])
    # print(df)
    print(f"from stockvalue {stockTicker}")
    minDatePurchased = min(df['datePurchased'])
    print(f"earliest date for stock is {minDatePurchased}")
    aStocks = df['ticker'].unique()
    print(f"total distinct values in the stock is {aStocks}")
    now = datetime.today().date()
    daysinBetween= now - minDatePurchased.date()
    daysInYear = datetime(datetime.today().year+1,1,1)-datetime(minDatePurchased.year,1,1)
    dateSeries = pd.date_range( datetime(minDatePurchased.year,1,1).date(), periods=daysInYear.days,freq="D")
    dateSeriesFrame = pd.DataFrame(dateSeries)
    dateSeriesFrame.columns = ['dateSeries']
    dateSeriesFrame.dateSeries = pd.to_datetime(dateSeriesFrame.dateSeries)
    valueSeriesFrame = pd.merge(dateSeriesFrame, pd.DataFrame(aStocks),  how="cross")
    valueSeriesFrame.columns=['dateSeries','ticker']
    print(valueSeriesFrame.columns)
    valueSeriesFrame = pd.merge(valueSeriesFrame, df, left_on=['dateSeries','ticker'] , right_on=["datePurchased",'ticker'], how="left")
    print("------dateSeries-------")
    print(dateSeriesFrame.head)
    print("------df-------")
    print(df.head)
    print("------valueSeries-------")
    print(valueSeriesFrame.head)
    return df

def getHistoricalStockValue(stockData):
    
           
    df = pandas.DataFrame(stockData)
    df['ticker']=df.apply(lambda row: row['ticker'].upper(), axis=1)
    df['quantity']=pandas.to_numeric(df['quantity'])
    df['costBasis']=pandas.to_numeric(df['costBasis'])
    # print(df.dtypes)
    uniqueStocks = df['ticker'].unique()
    # uniqueStocks=[x.upper() for x in uniqueStocks]
    dfUniqueStocks= pandas.DataFrame(uniqueStocks,columns=['ticker'])
    minStockPurchaseYear = min(df['datePurchased']).year
    # print(f"mi purchase year is {minStockPurchaseYear}")
    maxStockPurchaseYear = datetime.today().year
    dfUniqueStocks['quantity']=0.00
    dfUniqueStocks['costBasis']=0.00
    # print("print(dfUniqueStocks)")
    # print(dfUniqueStocks)
    dfT = pandas.DataFrame(pandas.date_range(datetime(minStockPurchaseYear,1,1).date(), periods=(datetime(maxStockPurchaseYear,12,31)-datetime(minStockPurchaseYear,1,1)).days,freq="D"))
    dfT.columns=['datePurchased']
    dfV = pandas.merge(dfT, dfUniqueStocks, how = 'cross')
    df['datePurchased']=pandas.to_datetime(df['datePurchased'])
    dfV=pandas.concat([df,dfV])
    dfV=dfV.groupby(['datePurchased','ticker']).agg({'quantity':'sum','costBasis':'sum'}).reset_index()
    # print(f"after groupby")
    # print(dfV)
    dfV= dfV.sort_values(by=['ticker','datePurchased'])
    dfV['quantity']=dfV['quantity'].fillna(0)
    dfV['costBasis']=dfV['costBasis'].fillna(0)
    dfV['totalCost']=dfV['quantity']*pandas.to_numeric(dfV['costBasis'])
    dfV['cumQuantity'] = dfV.groupby(['ticker'])['quantity'].cumsum()
    dfV['cumCost']=dfV.groupby(['ticker'])['totalCost'].cumsum()
    # print("print(dfV)")
    # print(dfV[dfV['cumQuantity']>0.0].head)
    
    uniqueStocks=numpy.append(uniqueStocks,['ABCD'])
    stockData = yfinance.download(uniqueStocks.tolist(), datetime(minStockPurchaseYear,1,1).date(), datetime(maxStockPurchaseYear,12,31).date())
    # print("print(stockData)")
    # print(stockData)
    stockDataFrame = pandas.DataFrame(stockData)['Close'].reset_index().rename(columns={'index':'date'})
    # print(f"mainstockframe")
    # print(stockDataFrame.head)

    # if type(stockDataFrame) ==pandas.DataFrame:
    #     stockDF = pandas.concat([stockDF,pandas.DataFrame(pandas.DataFrame(stockData)['Close'].rename('ticker'))])
    # tempstockDataFrame = pandas.DataFrame(pandas.DataFrame(stockData)['Close'].rename('ticker'))

    stockNFDataframeColumns = ['date','stockclosevalue','tickername']
    stockNFDataframe = pandas.DataFrame(columns = stockNFDataframeColumns)
    # print(stockNFDataframe)
    stockSplitDataframeColumns =['splitdate','stocksplits','tickername']
    stockSplitDataframeColumnsDataTypesDict = {'splitdate' : datetime,
        'stocksplits': float,
        'tickername': str,
    }
    # print(stockSplitDataframeColumnsDataTypesDict)
    stockSplitDataframe=pandas.DataFrame(columns=stockSplitDataframeColumns)
    # print(stockSplitDataframe)

    for ticker in uniqueStocks:
        # print(ticker)
        tempStockDf = pandas.DataFrame(stockDataFrame[['Date',ticker.upper()]]).rename(columns= {'Date':'date',ticker.upper():'stockclosevalue'})
        tempStockDf['tickername'] = ticker.upper()
        # print(f"Below is the tempDF")
        # print(tempStockDf.head)
        stockNFDataframe = pandas.concat([stockNFDataframe,tempStockDf])
        # tempStockSplitDataframe=pandas.DataFrame(yfinance.Ticker(ticker.upper()).splits).reset_index().rename(columns={'Date':'splitdate','Stock Splits':'stocksplits'})
        # tempStockSplitDataframe['splitdate']=pandas.to_datetime(tempStockSplitDataframe['splitdate'])
        # tempStockSplitDataframe['tickername']=ticker.upper()
        # stockSplitDataframe=pandas.concat([stockSplitDataframe,tempStockSplitDataframe])
        # print(stockSplitData)
    stockNFDataframe=stockNFDataframe[stockNFDataframe['tickername']!='ABCD']
    # print(f"print(stockNFDataframe.head)")
    # print(stockNFDataframe.head)
    # stockSplitDataframe['splitdate']=pandas.to_datetime(stockSplitDataframe['splitdate'],format='datetime62[ns]')
    # stockSplitDataframe['splitdate']=stockSplitDataframe['splitdate'].dt.tz_localize(None).apply(lambda x:x-timedelta(days=1))
    # stockSplitDataframe['tickername']=stockSplitDataframe['tickername'].astype('string')
    # print(stockSplitDataframe.head)

    # print("before merge")
    # print(dfV.head)
    # print("data types")
    # print(dfV.dtypes)
    # print("---")
    # print(stockNFDataframe.dtypes)
    dfV = pandas.merge(dfV, stockNFDataframe, left_on=['datePurchased','ticker'], right_on=['date','tickername'], how='left')
    dfV['cumValue'] = dfV.apply(lambda row: row['cumQuantity']*row['stockclosevalue'], axis=1)
    dfV=dfV.groupby(['date']).agg({'quantity':'sum','costBasis':'sum','cumQuantity':'sum','cumValue':'sum','cumCost':'sum'}).reset_index()
    dfV['date']=pandas.to_datetime(dfV['date'])
    # print(dfV[dfV['stockclosevalue'].notnull()].head)
    print(dfV.info(memory_usage = "deep"))
    return dfV


    # stockDataFrame= pandas.DataFrame(stockDataFrame['Close'][t].rename('ticker'))
    # stockDataFrame.rename = 'ticker'
    # print(type(stockDataFrame))
    # print(stockDataFrame)
    # print(type(stockDataFrame.loc[datetime(2022,12,1)]['ticker']))
    # dfV['StockCloseRate'] = dfV.apply(lambda row : stockLookup(row['ticker'],row['datePurchased'].date(), stockDataFrame), axis = 1 )
    # stockDataFrame.columns = ['dates','ticker']
    # stockDataFrame['ticker']=pandas.to_numeric(stockDataFrame['ticker'])
    # print(stockDataFrame)
    # print(stockDataFrame[.at('date'==datetime(2021,2,13),'ticker')])
    # print(stockDataFrame[stockDataFrame['dates'] ==datetime(2021,2,13).date()]['ticker'])


def portfolioTrend(portfolio):
    df = pd.DataFrame(portfolio)