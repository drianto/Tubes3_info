from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QRadioButton, QButtonGroup, QSpinBox,
    QScrollArea, QGroupBox, QSizePolicy
)
from PyQt5.QtCore import Qt

class CVAnalyzerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Info")
        self.setGeometry(600, 250, 800, 600)
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
        for i in reversed(range(self.result_container.count())):
            widget = self.result_container.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        # Result card with dummy data
        for i in range(self.topresult_spin.value()):
            self.result_container.addWidget(self.create_result_card(f"Person {i+1}", 1))

    def create_result_card(self, name, match_count):
        card = QGroupBox()
        layout = QVBoxLayout()
        layout.setSpacing(6)

        name_label = QLabel(f"<b>{name}</b>")
        match_label = QLabel(f"Matched <b>{match_count}</b> keyword(s)")
        summary_button = QPushButton("📄 Summary")
        view_button = QPushButton("👁️ View CV")

        summary_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        view_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(summary_button)
        btn_layout.addWidget(view_button)

        layout.addWidget(name_label)
        layout.addWidget(match_label)
        layout.addLayout(btn_layout)

        card.setLayout(layout)
        return card