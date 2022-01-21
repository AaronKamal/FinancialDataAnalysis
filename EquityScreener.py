# Aaron Kamal
# I pledge my honor that I have abided by the stevens honor system
# This code will indicate the best buy and sell times of a stock based on a MACD, technical levels, and moving averages
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import mplfinance as mpf
import matplotlib.dates as mdates
from pandas_datareader import data as pdr
import yfinance as yf
import datetime as dt


yf.pdr_override()
start= dt.datetime(2020,1,2)
now = dt.datetime.now()

print("DISCLAIMER:Every buy and sell signal shown here is only a recommendation and all investments should be conducted after thorough research!")
print("The chart starts from",start,"and goes to",now)
stock = input("Enter stock:")

df = pdr.get_data_yahoo(stock, start,now)
df["Close"].plot(label="Close", color= 'green', alpha = .5)

pivots=[]
dates=[]
counter = 0
lastPivot = 0

Range=[0,0,0,0,0,0,0,0,0,0]
dateRange=[0,0,0,0,0,0,0,0,0,0]

# This is where the technical levels should appear.
for i in df.index:
    currentMax=max(Range, default= 0)
    value = round(df["Close"][i],2)

    Range = Range[1:9]
    Range.append(value)
    dateRange = dateRange[1:9]
    dateRange.append(i)
    if currentMax==max(Range, default=0):
        counter+=1
    else:
        counter=0
    if counter==5:
        lastPivot=currentMax
        dateloc=Range.index(lastPivot)
        lastDate=dateRange[dateloc]
                    
        pivots.append(lastPivot)
        dates.append(lastDate)
print()

# This is setting up the MACD

ShortEMA= df.Close.ewm(span=12, adjust = False).mean()
df['short']= ShortEMA
        
LongEMA = df.Close.ewm(span=26, adjust = False).mean()
df['long']= LongEMA

# This produces the MACD line
MACD = (ShortEMA-LongEMA)*2
df['MACD']=MACD

#This produces the signal line
SignalLine=df.MACD.ewm(span=9,adjust=False).mean()
SignalLine=SignalLine*2
df['signal']=SignalLine

# These are the two moving averages       
twoEMA= df.Close.ewm(span=200, adjust=False).mean()
        
SMA=df.Close.ewm(span=9, adjust=False).mean()
df['SMA']=SMA
        
x= [start,now]
y = [0,0]
               
# This is when to produce a buy and sell signal based on my conditions
def signalFunction(data):
    buyList=[]
    sellList=[]
    flagLong= False
    flagShort = False
    for i in range(0, len(data)):
        if data['MACD'][i] > data['signal'][i] and data['MACD'][i]<0 and flagShort== False and flagLong==False and data['Close'][i]>data['SMA'][i]:
            buyList.append(data['Close'][i])
            sellList.append(np.nan)
            flagShort = True
        elif flagShort == True and data['MACD'][i] < data['signal'][i] and data['MACD'][i]>0 and data['Close'][i]>data['SMA'][i]:
            sellList.append(data['Close'][i])
            buyList.append(np.nan)
            flagShort = False
        else:
            buyList.append(np.nan)
            sellList.append(np.nan)
    return(buyList, sellList)
        
                        
df['Buy'] = signalFunction(df)[0]
df['Sell'] = signalFunction(df)[1]

# This is to make the graph easier to understand
plt.plot(twoEMA, label = '200 EMA', color = 'blue', alpha = 0.5)
plt.plot(SMA, label= 'Simple Moving Average', color = 'red', alpha = 0.5)
plt.plot(MACD, color = 'purple', label='MACD')
plt.plot(SignalLine, color = 'orange', label = 'Signal Line')
plt.plot(x,y, color = 'grey', label = 'Zero line')
    
plt.legend(bbox_to_anchor=(1,.25),loc='lower right', prop={'size': 6})

# This prints the buy and sell signal along with signal lines      
timeD=dt.timedelta(days=30)
for index in range(len(pivots)):
    print(str(pivots[index])+":"+str(dates[index]))

    plt.plot_date([dates[index],dates[index]+timeD],
                    [pivots[index],pivots[index]],linestyle= "-", linewidth=1, marker=",", color = 'black')
            
    plt.title('Technical Stock Levels with MACD Signal Line')
    plt.ylabel('Close Price')
    plt.scatter(df.index, df['Buy'], color='Green', marker='^', alpha = 1)
    plt.scatter(df.index, df['Sell'], color='Red', marker='v', alpha = 1)
plt.grid()
plt.show()

    

