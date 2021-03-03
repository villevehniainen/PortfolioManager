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

port.add_stock('NFLX', 30, "2019-5-1")
port.add_stock('MSFT', 30, "2019-1-17")
port.add_stock('KO', 1, "2021-1-9")
port.pf_value()
port.pf_returns()
port.get_greeks()
port.count_sharpe()
print(port.alpha)
print(port.beta)

'''
file_name = "portfolios.pickle"
open_file = open(file_name, "rb")
o = pickle.load(open_file)
for i in range(len(o)):
    if o[i].id == "villevv":
        pof = o[i]
pof.uptodate()
print(pof.pf)
pof.get_greeks()
print(pof.beta)
print(pof.value)

file_name = "portfolios.pickle"
open_file = open(file_name, "rb")
o = pickle.load(open_file)
for i in range(len(o)):
    if o[i].id == pof.id:
        o.remove(o[i])
        break
o.append(pof)
open_file.close()
with open("portfolios.pickle", 'wb') as output:
    pickle.dump(o, output)
output.close()
'''

