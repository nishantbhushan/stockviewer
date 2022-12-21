import pandas
from datetime import datetime, timedelta
import yfinance
# from pandas_datareader import data as pdr

stocks = [
    {
        "ticker" : 'AAPL',
        'datePurchased' :datetime.strptime('2021-03-30', '%Y-%m-%d').date(),
        'quantity':12.3,
        'costBasis':189.23
    },
    {
        'ticker':'T',
        'datePurchased' :datetime.strptime('2022-06-15', '%Y-%m-%d').date(),
        'quantity':122,
        'costBasis':18.23
    },
]


    
df = pandas.DataFrame(stocks)
uniqueStocks = df['ticker'].unique()
uniqueStocks=numpy.append(uniqueStocks,['ABCD'])
dfUniqueStocks= pandas.DataFrame(uniqueStocks,columns=['ticker'])
dfUniqueStocks['quantity']=0
dfUniqueStocks['costBasis']=0
print(dfUniqueStocks)
dfT = pandas.DataFrame(pandas.date_range(datetime(2021,1,1).date(), periods=(datetime(2022,12,31)-datetime(2021,1,1)).days,freq="D"))
dfT.columns=['datePurchased']
dfV = pandas.merge(dfT, dfUniqueStocks, how = 'cross')
df['datePurchased']=pandas.to_datetime(df['datePurchased'])
dfV=pandas.concat([df,dfV])
# dfV = pandas.merge(dfV,df ,left_on='DateSeries',right_on='datePurchased', how='left')
dfV= dfV.sort_values(by=['ticker','datePurchased'])
dfV['quantity']=dfV['quantity'].fillna(0)
dfV['costBasis']=dfV['costBasis'].fillna(0)
dfV['totalCost']=dfV['quantity']*dfV['costBasis']
dfV['cumQuantity'] = dfV.groupby(['ticker'])['quantity'].cumsum()
dfV['cumCost']=dfV.groupby(['ticker'])['totalCost'].cumsum()
print(dfV)

stockData = yfinance.download(uniqueStocks.tolist(), datetime(2021,1,1).date(), datetime(2022,12,31).date())
print(stockData)
stockDataFrame = pandas.DataFrame(stockData)['Close'].reset_index().rename(columns={'index':'date'})
print(f"mainstockframe")
print(stockDataFrame.head)

# if type(stockDataFrame) ==pandas.DataFrame:
#     stockDF = pandas.concat([stockDF,pandas.DataFrame(pandas.DataFrame(stockData)['Close'].rename('ticker'))])
# tempstockDataFrame = pandas.DataFrame(pandas.DataFrame(stockData)['Close'].rename('ticker'))

stockNFDataframeColumns = ['date','stockclosevalue','tickername']
stockNFDataframe = pandas.DataFrame(columns = stockNFDataframeColumns)
print(stockNFDataframe)
stockSplitDataframeColumns =['splitdate','stocksplits','tickername']
stockSplitDataframeColumnsDataTypesDict = {'splitdate' : datetime,
    'stocksplits': float,
    'tickername': str,
}
print(stockSplitDataframeColumnsDataTypesDict)
stockSplitDataframe=pandas.DataFrame(columns=stockSplitDataframeColumns)
print(stockSplitDataframe)

for ticker in uniqueStocks:
    tempStockDf = pandas.DataFrame(stockDataFrame[['Date',ticker.upper()]]).rename(columns= {'Date':'date',ticker.upper():'stockclosevalue'})
    tempStockDf['tickername'] = ticker.upper()
    print(f"Below is the tempDF")
    # print(tempStockDf.head)
    stockNFDataframe = pandas.concat([stockNFDataframe,tempStockDf])
    tempStockSplitDataframe=pandas.DataFrame(yfinance.Ticker(ticker.upper()).splits).reset_index().rename(columns={'Date':'splitdate','Stock Splits':'stocksplits'})
    # tempStockSplitDataframe['splitdate']=pandas.to_datetime(tempStockSplitDataframe['splitdate'])
    tempStockSplitDataframe['tickername']=ticker.upper()
    stockSplitDataframe=pandas.concat([stockSplitDataframe,tempStockSplitDataframe])
    # print(stockSplitData)


print(stockNFDataframe.head)
# stockSplitDataframe['splitdate']=pandas.to_datetime(stockSplitDataframe['splitdate'],format='datetime62[ns]')
stockSplitDataframe['splitdate']=stockSplitDataframe['splitdate'].dt.tz_localize(None).apply(lambda x:x-timedelta(days=1))
stockSplitDataframe['tickername']=stockSplitDataframe['tickername'].astype('string')
print(stockSplitDataframe.head)

dfV = pandas.merge(dfV, stockNFDataframe, left_on=['datePurchased','ticker'], right_on=['date','tickername'], how='left')
dfV = pandas.merge(dfV,stockSplitDataframe, left_on=['datePurchased','ticker'], right_on=['splitdate','tickername'],how='left')
mask = dfV['splitdate'].notnull()
notNullLocations = dfV.loc[mask, ['ticker', 'datePurchased','splitdate']]
print(notNullLocations)
# print(dfV[dfV['splitdate'].notnull()])
# dfV['tempbySplitDate'] = 
dfV['nextsplitdate'] = dfV.apply(lambda x: notNullLocations.loc[ \
                        (notNullLocations['ticker']==x['ticker']) & \
                        (notNullLocations['splitdate'] >= x['datePurchased']) \
                         , 'splitdate'].iloc[0] if not \
                        notNullLocations.loc[ \
                        (notNullLocations['ticker']==x['ticker']) & \
                        (notNullLocations['splitdate'] >= x['datePurchased'])].empty else None, axis=1)


dfV['cumQuantity'] = dfV.groupby(['ticker','nextsplitdate'])['quantity'].cumsum()
print(dfV.head)


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
dfV.to_csv('results.csv')

