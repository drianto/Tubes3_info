import sys
from PyQt5.QtWidgets import QApplication
from pages.main_menu import CVAnalyzerApp
from connection.db import MySQLConnection
from functions.pdf_reader import PDFReader
from mysql.connector import Error

import os
import threading


def preload_all():
    db = MySQLConnection()
    pdf_reader = PDFReader()
    db.connect("localhost", "cv", "root", "")
    try:
        with db as cursor:
            cursor.execute("SELECT cv_path FROM ApplicationDetail");
            records = cursor.fetchall();

            if not records:
                print("No records found.")
                return

            for row in records:
                path = os.path.abspath(f"../{row[0]}")
                pdf_reader.preload_pdf(path)
    except Error as e:
        print(e)

def main():
    db = MySQLConnection()
    threading.Thread(target=preload_all, daemon=True).start()
    app = QApplication(sys.argv)
    window = CVAnalyzerApp(db)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
