from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

from functions.section_scraper import SectionScraper

class SummaryWindow(QWidget):
    def __init__(self, applicantData, applicationDetail):
        super().__init__()
        self.setWindowTitle("CV Summary")
        self.setGeometry(800, 200, 400, 500)
        self.setStyleSheet("font-family: 'Segoe UI'; font-size: 13px;")
        self.applicantData = applicantData
        self.applicationDetail = applicationDetail
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        title = QLabel("CV Summary")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        layout.addWidget(title)

        name = self.applicantData[1] + " " + self.applicantData[2]
        birth_date, address, phone = self.applicantData[3:]
        info_box = self.create_section(f"{name}\n\nBirthdate: {birth_date}\nAddress: {address}\nPhone: {phone}")
        layout.addWidget(info_box)

        cv_path = self.applicationDetail[2]
        section_scraper = SectionScraper()

        skills = "Skills:\n\n" + section_scraper.scrape_skills(cv_path)
        skill_box = self.create_section(skills)
        layout.addWidget(skill_box)

        jobs = "Job History:\n\n" + section_scraper.scrape_experience(cv_path)
        job_box = self.create_section(jobs)
        layout.addWidget(job_box)

        education = "Education:\n\n" + section_scraper.scrape_education(cv_path)
        edu_box = self.create_section(education)
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
