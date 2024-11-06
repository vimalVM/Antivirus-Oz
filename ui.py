import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

class AntivirusUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Ozone Antivirus")
        self.setFixedSize(600, 400)
        
        # Main layout
        main_layout = QHBoxLayout(self)
        
        # Sidebar layout with buttons
        sidebar = QVBoxLayout()
        sidebar.setSpacing(15)
        
        self.scan_button = QPushButton("Scan")
        self.protection_button = QPushButton("Protection")
        self.toolbox_button = QPushButton("Toolbox")
        
        # Style the buttons
        for button in [self.scan_button, self.protection_button, self.toolbox_button]:
            button.setFont(QFont("Arial", 14))
            button.setFixedHeight(40)
            button.setStyleSheet("""
                QPushButton {
                    background-color: #004d99;
                    color: white;
                    border: none;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #0066cc;
                }
                QPushButton:pressed {
                    background-color: #003366;
                }
            """)
        
        # Connect buttons to actions
        self.scan_button.clicked.connect(self.show_scan_message)
        self.protection_button.clicked.connect(self.show_protection_message)
        self.toolbox_button.clicked.connect(self.show_toolbox_message)
        
        # Add buttons to sidebar layout
        sidebar.addWidget(self.scan_button)
        sidebar.addWidget(self.protection_button)
        sidebar.addWidget(self.toolbox_button)
        sidebar.addStretch()
        
        # Main content area
        self.content_area = QLabel("Your PC is safe!\nOzone Antivirus has protected your computer")
        self.content_area.setAlignment(Qt.AlignCenter)
        self.content_area.setFont(QFont("Arial", 16))
        self.content_area.setStyleSheet("color: #ffffff;")
        
        # Style main content area
        content_container = QWidget()
        content_container.setStyleSheet("background-color: #0073e6; border-radius: 8px;")
        content_layout = QVBoxLayout(content_container)
        content_layout.addWidget(self.content_area)
        
        # Add sidebar and content area to main layout
        main_layout.addLayout(sidebar)
        main_layout.addWidget(content_container)
        
        # Apply main window styles
        self.setStyleSheet("background-color: #004080;")

    # Slot functions for button clicks
    def show_scan_message(self):
        self.content_area.setText("Quick Scan initiated!")

    def show_protection_message(self):
        self.content_area.setText("Protection settings are active!")

    def show_toolbox_message(self):
        self.content_area.setText("Toolbox is ready to use!")

# Run the application
app = QApplication(sys.argv)
window = AntivirusUI()
window.show()
sys.exit(app.exec_())
