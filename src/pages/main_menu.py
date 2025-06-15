from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QRadioButton, QButtonGroup, QSpinBox,
    QScrollArea, QGroupBox, QSizePolicy, QGridLayout, QGraphicsOpacityEffect
)
import os
import itertools
import webbrowser
from PyQt5.QtCore import (Qt, QPropertyAnimation)
from pages.summary import SummaryWindow

from mysql.connector import Error
from connection.db import MySQLConnection
from functions.searcher import Searcher
from functions.string_matcher.knuth_morris_pratt import KnuthMorrisPratt
from functions.string_matcher.boyer_moore import BoyerMoore
from functions.string_matcher.aho_corasick import AhoCorasick

class CVAnalyzerApp(QWidget):
    def __init__(self, connection: MySQLConnection):
        super().__init__()
        self.setWindowTitle("Info")
        self.setGeometry(600, 250, 1600, 1400)

        self.current_page = 0
        self.cards_per_page = 4
        self.all_results = []
        self.connection = connection
        self.dark_mode = False
        self.apply_theme()

        self.initUI()

    def initUI(self):
        main_layout = QVBoxLayout()
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)

        title = QLabel("Infokan CV")
        title.setObjectName("TitleLabel")
        title.setAlignment(Qt.AlignCenter)
        title.setObjectName("TitleLabel")
        main_layout.addWidget(title)

        keyword_layout = QHBoxLayout()
        keyword_label = QLabel("Keywords:")
        keyword_label.setFixedWidth(120)
        self.keyword_input = QLineEdit()
        self.keyword_input.setPlaceholderText("e.g. Python, HTML, React")
        keyword_layout.addWidget(keyword_label)
        keyword_layout.addWidget(self.keyword_input)
        main_layout.addLayout(keyword_layout)

        algo_layout = QHBoxLayout()
        algo_label = QLabel("Algorithm:")
        algo_label.setFixedWidth(120)
        self.kmp_radio = QRadioButton("KMP")
        self.bm_radio = QRadioButton("Boyer-Moore")
        self.ac_radio = QRadioButton("Aho-Corasick")
        self.kmp_radio.setChecked(True)

        self.algo_group = QButtonGroup()
        self.algo_group.addButton(self.kmp_radio)
        self.algo_group.addButton(self.bm_radio)
        self.algo_group.addButton(self.ac_radio)

        self.searcher = Searcher(self.connection, KnuthMorrisPratt())

        algo_layout.addWidget(algo_label)
        algo_layout.addWidget(self.kmp_radio)
        algo_layout.addWidget(self.bm_radio)
        algo_layout.addWidget(self.ac_radio)
        algo_layout.addStretch()
        main_layout.addLayout(algo_layout)

        topresult_layout = QHBoxLayout()
        topresult_label = QLabel("Top Matches:")
        topresult_label.setFixedWidth(120)
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

        time_layout = QHBoxLayout()
        time_layout.setAlignment(Qt.AlignCenter)
        self.scan_time_label = QLabel("")
        time_layout.addWidget(self.scan_time_label)
        main_layout.addLayout(time_layout)

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

        if len(self.keyword_input.text()) == 0: return

        selected_algo = self.algo_group.checkedButton()
        if selected_algo == self.kmp_radio:
            self.searcher.set_algorithm(KnuthMorrisPratt())
        elif selected_algo == self.bm_radio:
            self.searcher.set_algorithm(BoyerMoore())
        elif selected_algo == self.ac_radio:
            self.searcher.set_algorithm(AhoCorasick())

        res, exact_time, fuzzy_time = self.searcher.search(self.keyword_input.text(), self.topresult_spin.value())
        for a in res.values():
            print(a)
        print(exact_time, fuzzy_time)

        time_label = f"Exact Time: {round(exact_time, 2)} ms. Fuzzy Time: {round(fuzzy_time, 2)} ms."
        self.scan_time_label.setText(time_label)

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

        result_len = min(len(self.all_results), self.topresult_spin.value());

        start_index = self.current_page * self.cards_per_page
        end_index = min(start_index + self.cards_per_page, result_len)
        result_keys = itertools.islice(self.all_results.keys(), start_index, end_index)

        for i, data in enumerate(result_keys):
            try:
                with self.connection as cursor:
                    cursor.execute("SELECT * FROM ApplicantProfile WHERE applicant_id = " + str(self.all_results[data]["data"][0]));
                    applicant = cursor.fetchone();
                    card = self.create_result_card(applicant, self.all_results[data])
            except Error as e:
                card = None
                print(e)
            card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            row, col = i // 2, i % 2
            grid_layout.addWidget(card, row, col)
            self.fade_in_widget(card)

        grid_widget = QWidget()
        grid_widget.setLayout(grid_layout)

        container_layout.addWidget(grid_widget)

        if result_len < self.cards_per_page:
            container_layout.addStretch()

        total_pages = (result_len + self.cards_per_page - 1) // self.cards_per_page
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

    def fade_in_widget(self, widget, duration=400):
        effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(effect)

        animation = QPropertyAnimation(effect, b"opacity")
        animation.setDuration(duration)
        animation.setStartValue(0)
        animation.setEndValue(1)
        animation.start()

        widget._fade_animation = animation

    def create_result_card(self, applicantData, applicationDetail):
        card = QGroupBox()
        layout = QVBoxLayout()
        layout.setSpacing(6)

        name = applicantData[2]
        exact_occurrences = applicationDetail["exact_occurences"]
        fuzzy_occurrences = applicationDetail["fuzzy_occurences"]
        total_match_count = sum(exact_occurrences.values()) + sum(fuzzy_occurrences.values())
        pdf_path = applicationDetail["data"][2]

        name_label = QLabel(f"<b>{name}</b>")
        match_label = QLabel(f"<i>{total_match_count} Matched keywords:</i>")

        keyword_labels = []
        idx = 1
        found_occurences = {}
        for (keyword, count) in exact_occurrences.items():
            if(count > 0):
                label = QLabel(f"{idx}. {keyword}: {count} exact occurrence{'s' if count > 1 else ''}")
                found_occurences[keyword] = label
                keyword_labels.append(label)
                idx += 1
        idx = 1
        for (keyword, count) in fuzzy_occurrences.items():
            if(count > 0):
                if(keyword in found_occurences):
                    found_occurences[keyword].setText(found_occurences[keyword].text() + f", {count} fuzzy occurence{'s' if count > 1 else ''}")
                else:
                    idx += 1
                    label = QLabel(f"{idx}. {keyword}: {count} fuzzy occurrence{'s' if count > 1 else ''}")
                    keyword_labels.append(label)

        summary_button = QPushButton("📄 Summary")
        view_cv_button = QPushButton("👁️ View CV")

        summary_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        view_cv_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        summary_button.clicked.connect(lambda: self.open_summary_window(applicantData, applicationDetail["data"]))
        view_cv_button.clicked.connect(lambda: self.open_view_cv_window(pdf_path))

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(summary_button)
        btn_layout.addWidget(view_cv_button)

        layout.addWidget(name_label)
        layout.addWidget(match_label)
        for label in keyword_labels:
            layout.addWidget(label)
        layout.addLayout(btn_layout)

        card.setLayout(layout)
        return card

    def open_summary_window(self, applicantData, applicationDetail):
        self.summary_window = SummaryWindow(applicantData, applicationDetail)
        self.summary_window.show()

    def open_view_cv_window(self, path):
        webbrowser.open(os.path.abspath("../"+path))

    def apply_theme(self):
        self.setStyleSheet("""

            QWidget {
                font-family: 'Segoe UI', sans-serif;
                font-size: 20px;
                background-color: #f0f4f8;
                color: #000000;
            }

            QLabel {
                font-size: 20px;
            }

            QLabel#TitleLabel {
                font-size: 32px;
                font-weight: 700;
                color: #0d47a1;
            }

            QLineEdit {
                padding: 6px 10px;
                border: 1px solid #ccc;
                border-radius: 6px;
                background-color: white;
            }

            QLineEdit:focus {
                border: 1px solid #1976d2;
                background-color: #e3f2fd;
            }

            QPushButton {
                background-color: #1976d2;
                color: white;
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 16px;
            }

            QPushButton:hover {
                background-color: #1565c0;
            }

            QPushButton:disabled {
                background-color: #90a4ae;
                color: #eceff1;
            }

            QGroupBox {
                border: 1px solid #ddd;
                border-radius: 12px;
                padding: 16px;
                background-color: #ffffff;
            }

            QRadioButton {
                padding: 2px 6px;
            }

            QSpinBox {
                padding: 4px;
                border-radius: 6px;
                background-color: white;
                border: 1px solid #ccc;
            }

            QScrollArea {
                border: none;
            }
        """)
