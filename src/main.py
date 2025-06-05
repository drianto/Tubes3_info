import sys
from PyQt5.QtWidgets import QApplication
from pages.main_menu import CVAnalyzerApp 

def main():
    app = QApplication(sys.argv)       
    window = CVAnalyzerApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
