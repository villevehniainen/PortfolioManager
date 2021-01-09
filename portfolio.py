import pandas as pd
import yfinance as yf
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm
import datetime
from datetime import date
import numpy as np
from datetime import datetime

'''
This class is used for creating and handling the user's portfolio with different methods.
'''


class Portfolio:

    def __init__(self, id):
        self.id = id
        self.stocks = {}
        self.omxh = self.find_omxh()
        self.sp500 = self.find_sp500()
        self.pf = self.create_pf()
        self.value = self.pf_value()
        self.alpha = 0.0
        self.beta = 0.0
        self.sharpe = 0.0

    def find_omxh(self):
        # Create a dataframe of OMXH Helsinki (currently not used in any methods as I prefer using sp500
        # as a market portfolio)
        tc = yf.Ticker('^OMXH25')
        helsinki = tc.history(period='5y')['Close']
        helsinki = helsinki.rename("Market")
        #df = pricedata.to_frame()
        #df.reset_index(level=0, inplace=True)
        #df['Return'] = df['Close'].pct_change()
        return helsinki

    def find_sp500(self):
        # Create a dataframe of sp500 which is used as a market portfolio in regressions
        tc = yf.Ticker('^GSPC')
        today = datetime.now()
        sp = tc.history(start = "2016-01-11", end = today)['Close']
        sp = sp.rename("Market")
        #df = sp.to_frame()
        #df.reset_index(level=0, inplace=True)
        #df['Return'] = df['Close'].pct_change()
        return sp

    def add_stock(self, tcker, amount, day):
        # adds a stock into the portfolio
        day = str(day)
        day = datetime.strptime(day, '%Y-%m-%d')
        today = datetime.now()
        delta = today - day
        if tcker in self.stocks:
            self.stocks[tcker] += amount
        else:
            self.stocks[tcker] = amount
        stock = yf.Ticker(tcker)
        # If the difference between the stock purchase and current date is less than 2 days, I just add
        # the latest value of the stock into the portfolio's last value
        if delta.days < 2:
            pricehistory = stock.history(period = '1d')
            prices = pricehistory['Close']
            price = float(prices[-1])
            price = price * amount
            self.pf['Value'].iloc[-1] += price
        # If there is a bigger difference then I will increase the portfolio's value for every day that
        # the stock was owned
        else:
            pricehistory = stock.history(start = day, end = today)['Close']
            pricehistory = pricehistory * amount
            self.pf['Value'] = self.pf['Value'].fillna(0)
            self.pf = pd.concat([self.pf, pricehistory], axis = 1)
            self.pf['Close'] = self.pf['Close'].fillna(0)
            self.pf['Value'] = self.pf['Value'] + self.pf['Close']
            self.pf = self.pf.drop(columns='Close')


    def sell_stock(self, ticker, amount):
        # This method performs stock selling and returns a message according to what has been performed
        stock = yf.Ticker(ticker)
        if ticker in self.stocks:
            if amount >= self.stocks[ticker]:
                pricehistory = stock.history(period='1d')
                prices = pricehistory['Close']
                price = float(prices[-1])
                price = price * self.stocks[ticker]
                self.pf['Value'].iloc[-1] -= price
                self.stocks.pop(ticker)
                return "Removed all shares of " + ticker + " from your portfolio."
            elif amount < self.stocks[ticker]:
                pricehistory = stock.history(period='1d')
                prices = pricehistory['Close']
                price = float(prices[-1])
                price = price * amount
                self.pf['Value'].iloc[-1] -= price
                self.stocks[ticker] -= amount
                ring = "Removed " + str(amount) + " shares of " + ticker + " from your portfolio."
                return ring
        else:
            return "Did not find a stock with that ticker from your portfolio."




    def create_pf(self):
        # Creates a portfolio dataframe that first has only the market portfolio and a column full of zeros
        # as the user does not have any stocks in the portfolio yet
        self.pf = self.omxh
        nuls = self.pf * 0
        nuls = nuls.rename('Value')
        self.pf = pd.concat([self.pf, nuls], axis = 1)
        self.market_returns()
        return self.pf

    def market_returns(self):
        # Creates a daily, monthly and annual market return columns to the portfolio dataframe
        self.pf['Daily Market Return'] = self.pf['Market'].pct_change(1)
        self.pf['Monthly Market Return'] = self.pf['Market'].pct_change(21)
        self.pf['Annual Market Return'] = self.pf['Market'].pct_change(252)

    def pf_value(self):
        self.value = self.pf['Value'].iloc[-1]
        return self.value

    def pf_returns(self):
        # Creates a daily, monthly and annual return and excess return columns to the portfolio dataframe
        self.pf['Daily Return'] = self.pf['Value'].pct_change(1)
        self.pf['Daily Excess'] = self.pf['Daily Return'] - self.pf['Daily Market Return']
        self.pf['Monthly Return'] = self.pf['Value'].pct_change(21)
        self.pf['Annual Return'] = self.pf['Value'].pct_change(252)
        self.pf['Monthly Excess'] = self.pf['Monthly Return'] - self.pf['Monthly Market Return']
        self.pf['Annual Excess'] = self.pf['Annual Return'] - self.pf['Annual Market Return']

    def get_greeks(self):
        # Does a regression for beta and alpha, currently using only daily returns, so the program shows
        # daily alpha but this can be modified in the future
        self.pf = self.pf.replace(np.inf, np.nan)
        df = self.pf.dropna()
        y = df['Daily Market Return']
        x = df['Daily Return']
        #col_size = x.size * -1
        #y = y.iloc[col_size:]
        x = sm.add_constant(x)
        mod = sm.OLS(y,x)
        res = mod.fit()
        greeks = res.params
        self.alpha = round(greeks[0] * 100,5)
        self.beta = round(greeks[1] * 100,3)

    def count_sharpe(self):
        # Counts the sharpe ratio for the portfolio
        vola = self.pf['Daily Excess'].std()
        avg = self.pf['Daily Return'].mean()
        self.sharpe = avg/vola
        self.sharpe = round(self.sharpe, 3)


    def uptodate(self):
        # Updates the portfolio. For example, if the user has not logged in for a few days, the portfolio
        # has to be update for the days between the last portfolio update and the current day
        from datetime import timedelta
        today = datetime.now()
        last = self.pf.index[-1] + timedelta(days=2)
        difference = today - last
        if difference.days < 3:
            pass
        else:
            market = yf.Ticker('^GSPC')
            sp = market.history(start=last, end=today)['Close']
            sp = sp.rename('Market')
            nuls = sp * 0
            nuls = nuls.rename('Value')
            sp = pd.concat([sp, nuls], axis=1)
            for tcker, amount in self.stocks.items():
                stock = yf.Ticker(tcker)
                df = stock.history(start=last, end=today)['Close']
                df = df * amount
                sp['Value'] = sp['Value'].fillna(0)
                sp = pd.concat([sp, df], axis=1)
                sp['Close'] = sp['Close'].fillna(0)
                sp['Value'] = sp['Value'] + sp['Close']
                sp= sp.drop(columns='Close')
            self.pf = self.pf.append(sp)
            self.market_returns()
            self.pf_returns()





