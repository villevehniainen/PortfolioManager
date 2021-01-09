from logscreen import App
import sys
from PyQt5.QtWidgets import QApplication
from portfolio import Portfolio
import pickle

def main():
    global app
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()