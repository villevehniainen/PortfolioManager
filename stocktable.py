from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
'''
In this class a table is created which shows the stocks that the user owns and there are columns for
stock ticker, company name, share price, daily return, number of shares owned and the value of shares owned.
'''

class Stocktable(QWidget):
    def __init__(self, data):
        super(Stocktable, self).__init__()
        self.data = data
        self.title = 'Stock table'
        self.left = 500
        self.top = 200
        self.width = 900
        self.height = 550


        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createTable()

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

        self.show()

    def createTable(self):
        #Table is created in this method by using the data created in infopage class.
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(len(self.data))
        self.tableWidget.setColumnCount(len(self.data[0]))
        columns = ['Ticker', 'Company name', 'Share price', 'Daily return', 'Shares owned', 'Value of shares']
        self.tableWidget.setHorizontalHeaderLabels(columns)
        for i in range(len(self.data)):
            for j in range(len(self.data[0])):
                self.tableWidget.setItem(i, j, QTableWidgetItem(self.data[i][j]))
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(
            QHeaderView.Stretch)




