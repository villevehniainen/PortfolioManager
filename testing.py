import pandas as pd
import yfinance as yf
import datetime
from datetime import date
from portfolio import Portfolio
from datetime import timedelta
from datetime import datetime
import pickle
'''
tesla = yf.Ticker('TSLA')
tdate = datetime.datetime(2020,5,17)
adate = datetime.datetime(2021,1,1)
today = date.today()
apple = yf.Ticker('AAPL')
teslaprice = tesla.history(start = tdate, end= today)['Close']
appleprice = apple.history(start = adate, end = today)['Close']
appleprice = appleprice.rename("Price")
df = pd.concat([teslaprice, appleprice], axis=1)
df['Price'] = df['Price'].fillna(0)
df["Close"] = df['Close'] + df['Price']
df = df.drop(columns=['Price'])
msft = yf.Ticker('MSFT')
mdate = datetime.datetime(2021,1,8)
msftprice = msft.history(start = mdate, end = today)['Close']
msftprice = msftprice.rename("Price")
msftprice = msftprice * 2
df = pd.concat([df, msftprice], axis=1)
print(df)
'''
port = Portfolio("Testi")

port.add_stock('AAPL', 2, "2020-5-1")
port.add_stock('MSFT', 3, "2021-03-03")
port.pf_value()
port.pf_returns()
port.get_greeks()
port.count_sharpe()
pd.set_option('display.max_rows', port.pf.shape[0]+1)
print(port.pf)
print(port.alpha)
print(port.beta)
print(port.sharpe)
print(port.value)
'''
file_name = "portfolios.pickle"
open_file = open(file_name, "rb")
o = pickle.load(open_file)
for i in range(len(o)):
    if o[i].id == "villevv":
        pof = o[i]
pof.add_stock("KO", 50, "2021-1-9")
print(pof.pf)
'''

