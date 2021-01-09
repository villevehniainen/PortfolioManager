from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QMessageBox, QDateEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize, Qt, QDate, QDateTime
import yfinance as yf
from infopage import Infopage
import pandas as pd
import datetime
from datetime import date
from portfolio import Portfolio

'''
This class asks user to add stocks to their portfolio. User can input the stock ticker, amount of shares
and when the stocks were bought. User can add as many stocks as they want and they can end adding the stocks
by clicking the 'finished' button.
'''


class Addstocks(QWidget):

    def __init__(self, pf):
        self.counter = 0
        self.pf = pf
        super(Addstocks, self).__init__()
        self.setMinimumSize(QSize(300, 230))
        self.resize(550, 320)
        self.setWindowTitle("Add stocks")

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.darkCyan)  # darkcyan
        self.setPalette(p)

        label1 = QLabel("Enter a stock ticker:", self)
        self.ticker = QLineEdit(self)
        self.ticker.move(270, 20)
        self.ticker.resize(200, 32)
        label1.move(20, 25)

        label2 = QLabel("How many shares?", self)
        self.amount = QLineEdit(self)
        self.amount.move(270, 80)
        self.amount.resize(200, 32)
        label2.move(20, 85)

        label3 = QLabel("When you bought it?", self)
        self.date = QDateEdit(self)
        self.date.move(270, 140)
        self.date.resize(200, 32)
        self.date.setDate(QDate.currentDate())

        label3.move(20, 145)
        self.date.editingFinished.connect(self.date_method)

        pybutton = QPushButton('Add a stock', self)
        pybutton.clicked.connect(self.click)
        pybutton.resize(200, 32)
        pybutton.move(270, 200)

        pybutton2 = QPushButton('Finished', self)
        pybutton2.clicked.connect(self.click1)
        pybutton2.resize(200, 32)
        pybutton2.move(270, 260)

    def date_method(self):
        # Change the date received by the user into a correct form
        self.counter += 1
        value = self.date.date()
        self.day = value.toPyDate()

    def click(self):
        # Finds the ticker from Yahoo Finance and checks that the number of stocks owned is legit.
        # Also checks that the date chosen is a legitimate.
        # self.counter is used because editingFinished.connect does not work if the user does not touch the
        # date picker at all. Thus, the program needs to have a date even though the date_method has not been
        # activated.
        if self.counter == 0:
            value = QDate.currentDate()
            self.day = value.toPyDate()
        today = date.today()
        delta = today - self.day
        if delta.days < 0:
            QMessageBox.about(self, "Error", "The date you gave is incorrect.")
        else:
            self.stock = self.ticker.text()
            self.am = self.amount.text()
            tc = yf.Ticker(self.stock)
            pricedata = tc.history(period='5y')['Close']
            if len(pricedata) > 0:
                try:
                    self.am = float(self.am)
                    if self.am < 0.01:
                        QMessageBox.about(self, "Error", "Incorrect amount!")
                    else:
                        self.pf.add_stock(self.stock, self.am, self.day)
                        QMessageBox.about(self, "Success", "Stock added!")
                        self.amount.clear()
                        self.ticker.clear()
                except ValueError:
                    QMessageBox.about(self, "Error", "Incorrect amount!")

            else:
                QMessageBox.about(self, "Error", "Did not find any data for that stock.")

    def click1(self):
        #counts the different ratios for the portfolio and launches the new window
        self.pf.pf_value()
        self.pf.pf_returns()
        self.pf.get_greeks()
        self.pf.count_sharpe()
        self.next_window = Infopage(self.pf)
        self.next_window.show()
        self.close()