import pandas as pd
from pandas import DataFrame, read_csv
import datetime
import numpy as np
import os
from stockstats import StockDataFrame
import math
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import csv


ret = 0
fee = 0
lev = 0
long_trades = []
short_trades = []

brokerage=0.0001
maxLeverge=10

data_1d=data_4h=data_60min=data_30min=data_15min=data_5min=data_1min=None


def take_long_Position(entryprice,stop,target,i,data_timeframe,data_1min,lst):
	global position,pnl,nrows,timestamp1,timestamp2,ret,fee,lev
	price=entryprice
	datetime_object = datetime.datetime.strptime(data_timeframe[i-1:i].index[0],'%Y-%m-%d %H:%M:%S+05:30')
	a = datetime_object.replace(minute=15)
	a = a.replace(hour=9)
	a = a.strftime('%Y-%m-%d %H:%M:%S+05:30')
	j = 0

	try:
		i = data_1min.index.get_loc(a)+1
	except:
		return


	t = data_1min[i+j:i+j+1].index[0]

	diff=abs(stop-price)

	while True and (i+j+2)<nrows:
		j = j+1
		if(data_1min['low'][i+j:i+j+1].iloc[0]<stop):
			lev = min(0.01*entryprice/diff,maxLeverge)
			fee = lev*brokerage
			ret = -100*fee-(100*diff*lev/entryprice)
			pnl3.append((time,ret/100))
			pnl.append((time,ret/100))
			long_trades.append((time,ret/100,lst))
			break

		elif(data_1min['high'][i+j:i+j+1].iloc[0]>target):
			lev = min(0.01*entryprice/diff,maxLeverge)
			fee = lev*brokerage
			ret = -100*fee+(100*diff*lev/entryprice)*abs(price-target)/abs(price-stop)
			pnl3.append((time,ret/100))
			pnl.append((time,ret/100))
			long_trades.append((time,ret/100,lst))
			break
	return



def take_short_Position(entryprice,stop,target,i,data_15min,data_1min,lst):
	global position,pnl,nrows,timestamp3,timestamp4,ret,fee,lev
	
	price=entryprice
	datetime_object = datetime.datetime.strptime(data_timeframe[i-1:i].index[0],'%Y-%m-%d %H:%M:%S+05:30')
	a = datetime_object.replace(minute=15)
	a = a.replace(hour=9)
	a = a.strftime('%Y-%m-%d %H:%M:%S+05:30')
	j = 0

	try:
		i = data_1min.index.get_loc(a)+1
	except:
		return

	t = data_1min[i+j:i+j+1].index[0]

	diff=abs(stop-price)
	while True and (i+j+1)<nrows:
		j = j+1
		if(data_1min['high'][i+j:i+j+1].iloc[0]>stop):
			lev = min(0.01*entryprice/diff,maxLeverge)
			fee = lev*brokerage
			ret = -100*fee-(100*diff*lev/entryprice)

			pnl4.append((time,ret/100))
			pnl.append((time,ret/100))
			short_trades.append((time,ret/100,lst))
			break
		elif(data_1min['low'][i+j:i+j+1].iloc[0]<target):
			lev = min(0.01*entryprice/diff,maxLeverge)
			fee = lev*brokerage
			ret = -100*fee+(100*diff*lev/entryprice)*abs(price-target)/abs(price-stop)
			pnl4.append((time,ret/100))
			pnl.append((time,ret/100))
			short_trades.append((time,ret/100,lst))
			break
	return

def strategy():
	global ret,fee,lev
	global data_1d,data_4h,data_60min,data_30min,data_15min,data_5min,data_1min
	i = 0
	

	#THIS CAN BE ANY DATAFRAME DEPENDING ON STRATEGY
	data_timeframe=data_60min
	data_timeframe = StockDataFrame.retype(data_timeframe)

	#ITERATE OVER DATAFRAME
	for row in data_timeframe.iterrows():
		i=i+1

		if(i>1 and data_timeframe[i-1:i].index[0] < '2019-06-00 00:00:00'):
			# DEPENDING ON STRATEGY LOGIC CALL take_short_Position() FUNCTION FOR SHORT TRADES AND take_long_Position() FOR LONG TRADES AFTER SPECIFYING entryprice, STOPLOSS AND TARGET






#THIS LIST CONTAINS STOCKS THAT WE WANT TO TEST
stock_list = ['4278529UBL', '582913MRF', '3924993NMDC', '1102337SRTRANSFIN', '794369SHREECEM', '1041153MARICO', '112129BHEL', '4454401NHPC', '3771393DLF', '2865921INDIGO', '758529SAIL', '3689729PAGEIND', '197633DABUR', '78081BAJAJHLDNG', '1076225MOTHERSUMI', '579329BANDHANBNK', '2748929OFSS', '4343041TATAMTRDVR', '4774913ICICIPRULI']


#CONTAINS DATA FROM 2019-
data_after_2019 = ['N101/'+x for x in stock_list]

#CONTAINS DATA FROM 2017-19
data_before_2019 = ['N103/'+x for x in stock_list]


lst = [[24,84,14,4,5]]
ccc=0

for a1 in range(0,len(stock_list)):


	print(stock_list[a1])


	data_1min = pd.concat([pd.read_csv(data_before_2019[a1] + os.sep + '1min.csv',index_col=0),pd.read_csv(data_after_2019[a1] + os.sep + '1min.csv',index_col=0)])
	data_30min = pd.concat([pd.read_csv(data_before_2019[a1] + os.sep + '30min.csv',index_col=0),pd.read_csv(data_after_2019[a1] + os.sep + '30min.csv',index_col=0)])
	data_15min = pd.concat([pd.read_csv(data_before_2019[a1] + os.sep + '15min.csv',index_col=0),pd.read_csv(data_after_2019[a1] + os.sep + '15min.csv',index_col=0)])
	data_5min = pd.concat([pd.read_csv(data_before_2019[a1] + os.sep + '5min.csv',index_col=0),pd.read_csv(data_after_2019[a1] + os.sep + '5min.csv',index_col=0)])
	data_60min = pd.concat([pd.read_csv(data_before_2019[a1] + os.sep + '60min.csv',index_col=0),pd.read_csv(data_after_2019[a1] + os.sep + '60min.csv',index_col=0)])
	data_1d = pd.concat([pd.read_csv(data_before_2019[a1] + os.sep + '1d.csv',index_col=0),pd.read_csv(data_after_2019[a1] + os.sep + '1d.csv',index_col=0)])
	data_4h = pd.concat([pd.read_csv(data_before_2019[a1] + os.sep + '4h.csv',index_col=0),pd.read_csv(data_after_2019[a1] + os.sep + '4h.csv',index_col=0)])


	data_15min = StockDataFrame.retype(data_15min)
	data_60min = StockDataFrame.retype(data_60min)
	data_30min = StockDataFrame.retype(data_30min)
	data_1d = StockDataFrame.retype(data_1d)
	data_60min.get('dx')
	data_60min.get('macd')
	data_1d.get('dx')
	data_1d.get('macd')
	data_15min.get('macd') # calculate MACD
	data_15min.get('rsi_14')
	data_15min.get('atr')
	data_30min.get('atr')
	data_15min.get('dx')
	data_15min['ATR'] = data_15min['tr'].ewm(span = 14).mean()
	data_30min['ATR'] = data_30min['tr'].ewm(span = 14).mean()

	nrows = data_1min.shape[0]
	nrows2 = data_15min.shape[0]


	data_15min['price'] = (data_15min['high']+data_15min['low']+data_15min['close'])/3
	data_15min['vprice'] = data_15min['price']*data_15min['volume']
	data_15min['vwap'] = data_15min['vprice'].rolling(min_periods=1, window = 100).sum()/data_15min['volume'].rolling(min_periods=1, window = 100).sum()


	data_30min['price'] = (data_30min['high']+data_30min['low']+data_30min['close'])/3
	data_30min['vprice'] = data_30min['price']*data_30min['volume']
	data_30min['vwap'] = data_30min['vprice'].rolling(min_periods=1, window = 100).sum()/data_30min['volume'].rolling(min_periods=1, window = 100).sum()

	data_60min['price'] = (data_60min['high']+data_60min['low']+data_60min['close'])/3
	data_60min['vprice'] = data_60min['price']*data_60min['volume']
	data_60min['vwap'] = data_60min['vprice'].rolling(min_periods=1, window = 100).sum()/data_60min['volume'].rolling(min_periods=1, window = 100).sum()

	data_1d['price'] = (data_1d['high']+data_1d['low']+data_1d['close'])/3
	data_1d['vprice'] = data_1d['price']*data_1d['volume']
	data_1d['vwap'] = data_1d['vprice'].rolling(min_periods=1, window = 100).sum()/data_1d['volume'].rolling(min_periods=1, window = 100).sum()


	df1 = data_15min['low']
	df2 = data_15min['high']
	df3 = data_15min['close']
	df1 = df1.rolling(14).min()
	df2 = df2.rolling(14).max()
	data_15min['STOK_14'] = ((df3 - df1) / (df2 - df1)) * 100

	df1 = data_60min['low']
	df2 = data_60min['high']
	df3 = data_60min['close']
	df1 = df1.rolling(14).min()
	df2 = df2.rolling(14).max()
	data_60min['STOK_14'] = ((df3 - df1) / (df2 - df1)) * 100

	pnl = []
	pnl3 = []
	pnl4 = []


	strategy()



	print("Toal long Trades with profit = %d" %sum(x[1] > 0 for x in pnl3))
	print("Total long Trades with loss = %d" %sum(x[1] < 0 for x in pnl3))
	newl1 = [x[1]+1 for x in pnl3]
	ret = 100*(np.prod(np.array(newl1))-1)
	print("Long Trades total return = %f" %ret)


	print("Total short Trades with profit = %d" %sum(x[1] > 0 for x in pnl4))
	print("Total short Trades with loss = %d" %sum(x[1] < 0 for x in pnl4))
	newl1 = [x[1]+1 for x in pnl4]
	ret = 100*(np.prod(np.array(newl1))-1)
	print("Short Trades total return = %f" %ret)
	

	print("Total Trades with profit = %d" %sum(x[1] > 0 for x in pnl4))
	print("Total Trades with loss = %d" %sum(x[1] < 0 for x in pnl4))
	newl1 = [x[1]+1 for x in pnl4]
	ret = 100*(np.prod(np.array(newl1))-1)
	print("Trades total return = %f" %ret)




print(long_trades)
print(short_trades)

print("Total Trades with profit = %d" %sum(x[1] > 0 for x in long_trades))
print("Total Trades with loss = %d" %sum(x[1] < 0 for x in long_trades))
newl1 = [x[1]+1 for x in long_trades]
ret = 100*(np.prod(np.array(newl1))-1)
print("total yearly return = %f" %ret)

long_trades = [x[1] for x in long_trades]
print('sharpe ratio : ' , np.nanmean(long_trades)/np.nanstd(long_trades)*np.sqrt(len(long_trades)))

print("Total Trades with profit = %d" %sum(x[1] > 0 for x in short_trades))
print("Total Trades with loss = %d" %sum(x[1] < 0 for x in short_trades))
newl1 = [x[1]+1 for x in short_trades]
ret = 100*(np.prod(np.array(newl1))-1)
print("total yearly return = %f" %ret)

long_trades = [x[1] for x in long_trades]