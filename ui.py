import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QStackedWidget, QFrame
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon
from PyQt5.QtCore import Qt

class AntivirusApp(QWidget):
    def __init__(self):
        super().__init__()

        # Main Window setup
        self.setWindowTitle("Baidu Antivirus")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background-color: #1a73e8;")

        # Layouts
        main_layout = QVBoxLayout()
        left_layout = QVBoxLayout()
        right_layout = QVBoxLayout()

        # Top bar
        top_bar = QLabel("Baidu Antivirus 2015     Free Forever")
        top_bar.setStyleSheet("color: white; font-size: 16px;")
        top_bar.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(top_bar)

        # Left Sidebar
        sidebar = QFrame()
        sidebar.setStyleSheet("background-color: #2a3b52;")
        sidebar_layout = QVBoxLayout(sidebar)

        scan_button = QPushButton("Scan")
        scan_button.setStyleSheet("color: white; font-size: 14px; background: transparent;")
        sidebar_layout.addWidget(scan_button)

        protection_button = QPushButton("Protection")
        protection_button.setStyleSheet("color: white; font-size: 14px; background: transparent;")
        sidebar_layout.addWidget(protection_button)

        toolbox_button = QPushButton("Toolbox")
        toolbox_button.setStyleSheet("color: #ff8c00; font-size: 14px; background: transparent;")
        sidebar_layout.addWidget(toolbox_button)

        # Add additional sidebar buttons for "Quarantine", "Trusted", and "Log"
        quarantine_button = QPushButton("Quarantine")
        quarantine_button.setStyleSheet("color: white; font-size: 12px; background: transparent;")
        sidebar_layout.addWidget(quarantine_button)

        trusted_button = QPushButton("Trusted")
        trusted_button.setStyleSheet("color: white; font-size: 12px; background: transparent;")
        sidebar_layout.addWidget(trusted_button)

        log_button = QPushButton("Log")
        log_button.setStyleSheet("color: white; font-size: 12px; background: transparent;")
        sidebar_layout.addWidget(log_button)

        # Add left sidebar to the main layout
        sidebar_layout.addStretch()
        main_layout.addWidget(sidebar, alignment=Qt.AlignLeft)

        # Center Area
        shield_icon = QLabel()
        shield_icon.setPixmap(QIcon("path_to_shield_icon.png").pixmap(100, 100))  # Set a shield icon here
        shield_icon.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(shield_icon)

        status_label = QLabel("Your PC is safe!")
        status_label.setStyleSheet("color: white; font-size: 24px; font-weight: bold;")
        status_label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(status_label)

        info_label = QLabel("Baidu Antivirus has protected your computer for 1 day")
        info_label.setStyleSheet("color: #b3c7f9; font-size: 14px;")
        info_label.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(info_label)

        # Quick Scan Button
        quick_scan_button = QPushButton("Quick Scan")
        quick_scan_button.setStyleSheet("background-color: #28a745; color: white; font-size: 16px; padding: 10px 20px;")
        right_layout.addWidget(quick_scan_button, alignment=Qt.AlignCenter)

        # Bottom Options
        scan_options = QLabel("Full Scan   |   Custom Scan")
        scan_options.setStyleSheet("color: white; font-size: 14px;")
        scan_options.setAlignment(Qt.AlignCenter)
        right_layout.addWidget(scan_options)

        # Adding layouts to main layout
        content_layout = QHBoxLayout()
        content_layout.addWidget(sidebar)
        content_layout.addLayout(right_layout)
        main_layout.addLayout(content_layout)

        self.setLayout(main_layout)


app = QApplication(sys.argv)
window = AntivirusApp()
window.show()
sys.exit(app.exec_())
