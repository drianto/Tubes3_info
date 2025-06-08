from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class ViewCVWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CV Overview")
        self.setGeometry(800, 200, 400, 500)
        self.setStyleSheet("font-family: 'Segoe UI'; font-size: 13px;")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        title = QLabel("CV Summary")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        layout.addWidget(title)