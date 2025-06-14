import sys
from PyQt5.QtWidgets import QApplication
from pages.main_menu import CVAnalyzerApp
from connection.db import MySQLConnection

def main():
    db = MySQLConnection()
    db.connect("localhost", "cv", "root", "")
    app = QApplication(sys.argv)
    window = CVAnalyzerApp(db)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
