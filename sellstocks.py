from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QMessageBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize, Qt
import yfinance as yf
import infopage
import pandas as pd
from portfolio import Portfolio

'''
In this class user can sell stocks and the program creates a informative message regards the success of
the selling
'''

class Sellstocks(QWidget):

    def __init__(self, pf):
        self.pf = pf
        super(Sellstocks, self).__init__()
        self.setMinimumSize(QSize(300, 230))
        self.resize(550, 320)
        self.setWindowTitle("Sell stocks")

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.darkCyan)  # darkcyan
        self.setPalette(p)

        label1 = QLabel("Enter a stock ticker:", self)
        self.ticker = QLineEdit(self)
        self.ticker.move(290, 15)
        self.ticker.resize(200, 32)
        label1.move(20, 25)

        label2 = QLabel("How many shares you want to sell?", self)
        self.amount = QLineEdit(self)
        self.amount.move(290, 75)
        self.amount.resize(200, 32)
        label2.move(20, 80)

        pybutton = QPushButton('Sell a stock', self)
        pybutton.clicked.connect(self.click)
        pybutton.resize(200, 32)
        pybutton.move(290, 140)

        pybutton2 = QPushButton('Finished', self)
        pybutton2.clicked.connect(self.click1)
        pybutton2.resize(200, 32)
        pybutton2.move(290, 200)

    def click(self):
        # when the user clicks 'sell a stock' button, the program moves here and sells the given amount of
        # shares of the stock
        stock = self.ticker.text()
        am = self.amount.text()
        txt = self.pf.sell_stock(stock, int(am))
        QMessageBox.about(self, "info", txt)


    def click1(self):
        # counts the different ratios for the portfolio and launches the infopage window
        self.pf.pf_value()
        self.pf.pf_returns()
        self.pf.get_greeks()
        self.pf.count_sharpe()
        self.next_window = infopage.Infopage(self.pf)
        self.next_window.show()
        self.close()