from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QMessageBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize, Qt
from PyQt5 import QtWidgets
from portfolio import Portfolio
import addstocks
import yfinance as yf
from sellstocks import Sellstocks
from stocktable import Stocktable
import pickle

'''
This class shows the user an infopage where user can see their portfolio's sharpe ratio, alpha, beta and
portfolio value. Through this window user can modify their portfolio by buying or selling stocks.
There is also a chance for the user to see all of their stocks and some information about them
in a neat table. 
'''

class Infopage(QWidget):

    def __init__(self, pf):
        self.pf = pf
        super(Infopage, self).__init__()
        self.setMinimumSize(QSize(300, 230))
        self.resize(550,350)
        self.setWindowTitle("ID information")

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.darkCyan)  # darkcyan
        self.setPalette(p)

        self.alphalabel = "Your portfolio's alpha is " + str(self.pf.alpha) + "%"
        label1 = QLabel(self.alphalabel, self)
        label1.move(70, 30)

        self.betalabel = "Your portfolio's beta is " + str(self.pf.beta)
        label2 = QLabel(self.betalabel, self)
        label2.move(70, 60)

        self.sharpelabel = "Your portfolio's sharpe is " + str(self.pf.sharpe)
        label3 = QLabel(self.sharpelabel, self)
        label3.move(70, 90)

        val = round(self.pf.value, 2)
        self.valuelabel = "Your portfolio's value is " + str(val) + "$"
        label4 = QLabel(self.valuelabel, self)
        label4.move(70, 120)

        pybutton1 = QPushButton('Buy a stock', self)
        pybutton1.clicked.connect(self.click)
        pybutton1.resize(200, 32)
        pybutton1.move(70, 185)

        pybutton2 = QPushButton('Sell a stock', self)
        pybutton2.clicked.connect(self.click1)
        pybutton2.resize(200, 32)
        pybutton2.move(70, 225)

        pybutton3 = QPushButton('Log out', self)
        pybutton3.clicked.connect(self.click2)
        pybutton3.resize(200, 32)
        pybutton3.move(70, 265)

        pybutton4 = QPushButton('Show my stocks', self)
        pybutton4.clicked.connect(self.click3)
        pybutton4.resize(200, 32)
        pybutton4.move(290, 185)

    def click(self):
        # Through this user can buy new stocks to their portfolio
        self.next_window = addstocks.Addstocks(self.pf)
        self.next_window.show()
        self.close()

    def click1(self):
        # Through this user can sell stocks from their portfolio
        self.next_window = Sellstocks(self.pf)
        self.next_window.show()
        self.close()

    def click2(self):
        # User logs out and the portfolio is saved into the pickle file
        file_name = "portfolios.pickle"
        open_file = open(file_name, "rb")
        o = pickle.load(open_file)
        for i in range(len(o)):
            if o[i].id == self.pf.id:
                o.remove(o[i])
                break
        o.append(self.pf)
        open_file.close()
        with open("portfolios.pickle", 'wb') as output:
            pickle.dump(o, output)
        output.close()
        self.close()

    def click3(self):
        # The contents for the table is created and assigned into the list 'data'
        # After that the program moves to show the table containing information about the user's stocks
        data = []
        for tcker, amount in self.pf.stocks.items():
            data_list = []
            data_list.append(tcker)
            tc = yf.Ticker(tcker)
            data_list.append(tc.info['shortName'])
            df = tc.history(period='5d')
            prices = df['Close']
            pricethen = float(prices[-2])
            pricenow = float(prices[-1])
            priceno = str(pricenow) + " $"
            data_list.append(priceno)
            daily_return = (pricenow - pricethen) / pricethen
            daily_return = daily_return * 100
            daily_return = round(daily_return, 2)
            daily_return = str(daily_return) + " %"
            data_list.append(daily_return)
            data_list.append(str(int(amount)))
            my_value = round(amount * pricenow,2)
            my_value = str(my_value) + " $"
            data_list.append(my_value)
            data.append(data_list)
        self.next_window = Stocktable(data)
        self.next_window.show()







