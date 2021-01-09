from PyQt5.QtWidgets import QApplication, QPushButton, QDialog, QLabel
from PyQt5.QtCore import pyqtSlot, Qt
import sys
from newaccount import Newaccount
from oldaccount import Oldaccount

'''
The program starts from here and the user has the chance to log into an existing account
or create a new account
'''


class App(QDialog):

    def __init__(self):
        super().__init__()
        self.title = 'Portfolio management system'
        self.left = 820
        self.top = 400
        self.width = 500
        self.height = 350
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.darkCyan)  # darkcyan
        self.setPalette(p)

        label1 = QLabel('Welcome to the PortfolioManager!', self)
        label1.move(70, 50)

        label2 = QLabel('Log in or create a new account.', self)
        label2.move(70, 90)

        button1 = QPushButton('Log in', self)
        button1.clicked.connect(self.on_click1)
        button1.move(70, 150)
        button1.resize(370, 32)
        button1.setStyleSheet("background-color: white; color: black; font-weight: 800; font-size: 22")

        button2 = QPushButton('Create a new account', self)
        button2.clicked.connect(self.on_click2)
        button2.move(70, 200)
        button2.resize(370, 32)
        button2.setStyleSheet("background-color: white; color: black; font-weight: 800; font-size: 22")

        self.show()

    @pyqtSlot()
    def on_click1(self):
        self.next_window = Oldaccount()
        self.next_window.show()

    def on_click2(self):
        self.next_window = Newaccount()
        self.next_window.show()
