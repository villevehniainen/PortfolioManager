from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QMessageBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize, Qt
from portfolio import Portfolio
from addstocks import Addstocks
import pickle
'''
A new account is created in this class and the program checks that there does not exist any portfolios with
the same ID before the new account is fully created
'''

class Newaccount(QWidget):

    def __init__(self):
        super(Newaccount, self).__init__()

        self.setMinimumSize(QSize(300, 230))
        self.resize(550,250)
        self.setWindowTitle("ID information")

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.darkCyan)  # darkcyan
        self.setPalette(p)

        label1 = QLabel("Enter your ID:", self)
        self.name = QLineEdit(self)
        self.name.move(250, 20)
        self.name.resize(200, 32)
        label1.move(20, 25)

        pybutton1 = QPushButton('OK', self)
        pybutton1.clicked.connect(self.click)
        pybutton1.resize(200, 32)
        pybutton1.move(250, 100)

        pybutton2 = QPushButton('Cancel', self)
        pybutton2.clicked.connect(self.click1)
        pybutton2.resize(200, 32)
        pybutton2.move(250, 155)

    def click(self):
        # Program checks the pickle file and gives an error message if there already exists a portfolio
        # with the same ID as what the user has just given
        not_found = True
        self.portfolioid = self.name.text()
        file_name = "portfolios.pickle"
        open_file = open(file_name, "rb")
        o = pickle.load(open_file)
        for i in range(len(o)):
            if o[i].id == self.portfolioid:
                not_found = False
                break
        open_file.close()
        if not_found:
            self.pf = Portfolio(self.portfolioid)
            self.next_window = Addstocks(self.pf)
            self.next_window.show()
            self.close()
        else:
            QMessageBox.about(self, "Error", "There already exists a portfolio with that ID.")

    def click1(self):
        self.close()