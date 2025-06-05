from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

def show_window():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(200, 200, 300, 300) 
    win.setWindowTitle("Main Window")

    win.show()
    sys.exit(app.exec_())