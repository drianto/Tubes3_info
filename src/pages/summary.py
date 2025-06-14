from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class SummaryWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CV Summary")
        self.setGeometry(800, 200, 400, 500)
        self.setStyleSheet("font-family: 'Segoe UI'; font-size: 13px;")
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        title = QLabel("CV Summary")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        layout.addWidget(title)

        info_box = self.create_section("Jawa Barak\n\nBirthdate: 32-13-202222\nAddress: Barak Kang Dedi\nPhone: 3336 7890")
        layout.addWidget(info_box)

        skill_box = self.create_section("Skills:\n\n[ Barak ]   [ OOO ]   [ Kang ]")
        layout.addWidget(skill_box)

        job_box = self.create_section("Job History:\n\nGuberneur\n209-2014\nMengirim ke barak")
        layout.addWidget(job_box)

        edu_box = self.create_section("Education:\n\nBrak\n2022–2021")
        layout.addWidget(edu_box)

        self.setLayout(layout)

    def create_section(self, text):
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #e0e0e0;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        label = QLabel(text)
        label.setWordWrap(True)
        label.setStyleSheet("font-size: 13px;")
        vbox = QVBoxLayout()
        vbox.addWidget(label)
        frame.setLayout(vbox)
        return frame
