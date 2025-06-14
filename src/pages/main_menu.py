from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QRadioButton, QButtonGroup, QSpinBox,
    QScrollArea, QGroupBox, QSizePolicy, QGridLayout
)
import os
import webbrowser
from PyQt5.QtCore import Qt
from pages.summary import SummaryWindow
from pages.view_cv import ViewCVWindow

from mysql.connector import Error
from connection.db import MySQLConnection
from functions.searcher import Searcher
from functions.string_matcher.knuth_morris_pratt import KnuthMorrisPratt
from functions.string_matcher.boyer_moore import BoyerMoore

class CVAnalyzerApp(QWidget):
    def __init__(self, connection: MySQLConnection):
        super().__init__()
        self.setWindowTitle("Info")
        self.setGeometry(600, 250, 800, 700)
        self.setStyleSheet("""
            QWidget {
                font-family: Segoe UI, sans-serif;
                font-size: 14px;
            }
            QPushButton {
                background-color: #1976d2;
                color: white;
                border-radius: 6px;
                padding: 6px 12px;
            }
            QPushButton:hover {
                background-color: #1565c0;
            }
            QGroupBox {
                border: 1px solid #ccc;
                border-radius: 10px;
                padding: 12px;
                background-color: #f9f9f9;
            }
        """)
        self.current_page = 0
        self.cards_per_page = 4
        self.all_results = []
        self.connection = connection
        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Infokan CV")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 28px; font-weight: 600; margin-bottom: 10px;")
        main_layout.addWidget(title)

        keyword_layout = QHBoxLayout()
        keyword_label = QLabel("Keywords:")
        keyword_label.setFixedWidth(100)
        self.keyword_input = QLineEdit()
        self.keyword_input.setPlaceholderText("e.g. Python, HTML, React")
        keyword_layout.addWidget(keyword_label)
        keyword_layout.addWidget(self.keyword_input)
        main_layout.addLayout(keyword_layout)

        algo_layout = QHBoxLayout()
        algo_label = QLabel("Algorithm:")
        algo_label.setFixedWidth(100)
        self.kmp_radio = QRadioButton("KMP")
        self.bm_radio = QRadioButton("Boyer-Moore")
        self.kmp_radio.setChecked(True)

        self.algo_group = QButtonGroup()
        self.algo_group.addButton(self.kmp_radio)
        self.algo_group.addButton(self.bm_radio)

        self.searcher = Searcher(self.connection, KnuthMorrisPratt())

        algo_layout.addWidget(algo_label)
        algo_layout.addWidget(self.kmp_radio)
        algo_layout.addWidget(self.bm_radio)
        algo_layout.addStretch()
        main_layout.addLayout(algo_layout)

        topresult_layout = QHBoxLayout()
        topresult_label = QLabel("Top Matches:")
        topresult_label.setFixedWidth(100)
        self.topresult_spin = QSpinBox()
        self.topresult_spin.setRange(1, 100)
        self.topresult_spin.setValue(5)
        topresult_layout.addWidget(topresult_label)
        topresult_layout.addWidget(self.topresult_spin)
        topresult_layout.addStretch()
        main_layout.addLayout(topresult_layout)

        self.search_button = QPushButton("🔍 Search")
        self.search_button.setFixedHeight(32)
        self.search_button.clicked.connect(self.search)
        main_layout.addWidget(self.search_button)

        self.result_area = QScrollArea()
        self.result_container = QVBoxLayout()
        self.result_container.setSpacing(12)

        self.result_widget = QWidget()
        self.result_widget.setLayout(self.result_container)
        self.result_area.setWidgetResizable(True)
        self.result_area.setWidget(self.result_widget)
        main_layout.addWidget(self.result_area)
        self.setLayout(main_layout)

    def search(self):

        selected_algo = self.algo_group.checkedButton()
        if selected_algo == self.kmp_radio:
            self.searcher.set_algorithm(KnuthMorrisPratt())
        elif selected_algo == self.bm_radio:
            self.searcher.set_algorithm(BoyerMoore())

        res, time = self.searcher.search(self.keyword_input.text(), self.topresult_spin.value())
        for a in res:
            print(a)
        print(time)


        self.all_results = res

        self.current_page = 0
        self.update_result_view()

    def update_result_view(self):
        for i in reversed(range(self.result_container.count())):
            widget = self.result_container.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        container_layout = QVBoxLayout()
        container_layout.setSpacing(10)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(20)
        grid_layout.setContentsMargins(10, 10, 10, 10)

        start_index = self.current_page * self.cards_per_page
        end_index = min(start_index + self.cards_per_page, len(self.all_results))
        results_to_show = self.all_results[start_index:end_index]

        for i, data in enumerate(results_to_show):
            try:
                with self.connection as cursor:
                    cursor.execute("SELECT * FROM ApplicantProfile WHERE applicant_id = " + str(data[0][1]));
                    applicant = cursor.fetchone();
                    card = self.create_result_card(applicant, data)
            except Error as e:
                # card = self.create_result_card("N/A", data)
                print(e)
            card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            row, col = i // 2, i % 2
            grid_layout.addWidget(card, row, col)

        grid_widget = QWidget()
        grid_widget.setLayout(grid_layout)

        container_layout.addWidget(grid_widget)

        if len(results_to_show) < self.cards_per_page:
            container_layout.addStretch()

        total_pages = (len(self.all_results) + self.cards_per_page - 1) // self.cards_per_page
        page_label = QLabel(f"Page {self.current_page + 1} of {total_pages}")
        page_label.setAlignment(Qt.AlignCenter)

        nav_layout = QHBoxLayout()
        prev_button = QPushButton("← Previous")
        next_button = QPushButton("Next →")

        prev_button.setEnabled(self.current_page > 0)
        next_button.setEnabled(end_index < len(self.all_results))

        prev_button.clicked.connect(self.go_to_prev_page)
        next_button.clicked.connect(self.go_to_next_page)

        nav_layout.addWidget(prev_button)
        nav_layout.addStretch()
        nav_layout.addWidget(page_label)
        nav_layout.addStretch()
        nav_layout.addWidget(next_button)

        nav_widget = QWidget()
        nav_widget.setLayout(nav_layout)
        nav_widget.setFixedHeight(50)

        container_layout.addWidget(nav_widget)

        page_widget = QWidget()
        page_widget.setLayout(container_layout)

        self.result_container.addWidget(page_widget)

    def go_to_next_page(self):
        self.current_page += 1
        self.update_result_view()

    def go_to_prev_page(self):
        self.current_page -= 1
        self.update_result_view()

    def create_result_card(self, applicantData, applicationDetail):
        card = QGroupBox()
        layout = QVBoxLayout()
        layout.setSpacing(6)

        name = applicantData[2]
        match_count = applicationDetail[1]
        pdf_path = applicationDetail[0][3]

        name_label = QLabel(f"<b>{name}</b>")
        match_label = QLabel(f"Matched <b>{match_count}</b> keyword(s)")
        summary_button = QPushButton("📄 Summary")
        view_cv_button = QPushButton("👁️ View CV")

        summary_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        view_cv_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        summary_button.clicked.connect(lambda: self.open_summary_window(applicantData, applicationDetail))
        view_cv_button.clicked.connect(lambda: self.open_view_cv_window(pdf_path))

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(summary_button)
        btn_layout.addWidget(view_cv_button)

        layout.addWidget(name_label)
        layout.addWidget(match_label)
        layout.addLayout(btn_layout)

        card.setLayout(layout)
        return card

    def open_summary_window(self, applicantData, applicationDetail):
        self.summary_window = SummaryWindow(applicantData, applicationDetail)
        self.summary_window.show()

    def open_view_cv_window(self, path):
        webbrowser.open(os.path.abspath("../data/"+path))
        # self.view_cv_window = ViewCVWindow()
        # self.view_cv_window.show()