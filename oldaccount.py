from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QMessageBox
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import QSize, Qt
from portfolio import Portfolio
from infopage import Infopage
import pickle

'''
In this class the user logs into their old account. The program checks the pickle file if there is an existing
account saved with the ID user has given. The program continues to the infopage class if there exists an
object with the given ID. Otherwise the program gives a message that there weren't any portfolio objects
with the given ID.
'''

class Oldaccount(QWidget):

    def __init__(self):
        super(Oldaccount, self).__init__()

        self.setMinimumSize(QSize(300, 230))
        self.resize(550,250)
        self.setWindowTitle("Log in")

        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), Qt.darkCyan)  # darkcyan
        self.setPalette(p)

        label1 = QLabel("Enter your existing ID:", self)
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
        # After the user clicks OK, the program checks the pickle file for a portfolio object
        # with a matching ID.
        file_name = "portfolios.pickle"
        found = False
        open_file = open(file_name, "rb")
        o = pickle.load(open_file)
        for i in range(len(o)):
            if o[i].id == self.name.text():
                pf = o[i]
                found = True
                break
        open_file.close()
        if found:
            pf.uptodate()
            pf.pf_value()
            pf.pf_returns()
            pf.get_greeks()
            pf.count_sharpe()
            self.next_window = Infopage(pf)
            self.next_window.show()
            self.close()
        else:
            QMessageBox.about(self, "Error", "Did not find any portfolios with that ID.")


    def click1(self):
        self.close()