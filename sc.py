import sys
import subprocess
import threading
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QTextEdit, QLabel, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, pyqtSignal, QObject

class Communicate(QObject):
    update_display = pyqtSignal(str)

class ClamAVScanner(QWidget):
    def __init__(self):
        super().__init__()
        
        # Setup communication and connect signal to display update method
        self.comm = Communicate()
        self.comm.update_display.connect(self.update_output_display)
        
        # Window setup
        self.setWindowTitle("ClamAV Scanner")
        self.setGeometry(200, 200, 800, 600)  # Initial window size
        
        # Main layout
        main_layout = QVBoxLayout()
        
        # Top layout (1/3 of window) with monitor image and buttons
        top_layout = QHBoxLayout()
        
        # Image on the top left
        self.image_label = QLabel()
        pixmap = QPixmap("/home/vimal/Desktop/pic/sn.png")  # Replace with actual path
        self.image_label.setPixmap(pixmap.scaled(150, 150, Qt.KeepAspectRatio))
        self.image_label.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        top_layout.addWidget(self.image_label, alignment=Qt.AlignLeft | Qt.AlignTop)
        
        # Buttons on the right of the image
        button_layout = QVBoxLayout()
        self.scan_button = QPushButton("Scan Default Directory")
        self.scan_button.clicked.connect(self.scan_default_directory)
        button_layout.addWidget(self.scan_button)
        
        self.custom_scan_button = QPushButton("Custom Scan")
        self.custom_scan_button.clicked.connect(self.custom_scan)
        button_layout.addWidget(self.custom_scan_button)
        
        # Cancel button to stop the scan
        self.cancel_button = QPushButton("Cancel Scan")
        self.cancel_button.clicked.connect(self.cancel_scan)
        self.cancel_button.setEnabled(False)
        button_layout.addWidget(self.cancel_button)
        
        top_layout.addLayout(button_layout)
        
        # Output display for scan results (keep it for real-time output from the scanner)
        self.output_display = QTextEdit()
        self.output_display.setReadOnly(True)
        
        # Add the top layout and output display to the main layout
        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.output_display, stretch=2)
        
        # Set main layout to window
        self.setLayout(main_layout)
        
        # Variables to manage the scanning process
        self.scan_process = None
        self.is_scanning = False
        self.infected_files = []  # To store the list of infected files

    def update_output_display(self, text):
        self.output_display.append(text)

    def scan_default_directory(self):
        default_directory = "C:/Desktop" if sys.platform == "win32" else "/home/vimal/Desktop"
        self.comm.update_display.emit(f"Scanning default directory: {default_directory}")
        self.start_scan(default_directory)

    def custom_scan(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Directory to Scan")
        if directory:
            self.comm.update_display.emit(f"Scanning custom directory: {directory}")
            self.start_scan(directory)

    def start_scan(self, directory):
        # Clear previous scan results
        self.output_display.clear()
        self.infected_files.clear()  # Clear infected files list
        
        # Disable scan buttons and enable cancel button
        self.scan_button.setEnabled(False)
        self.custom_scan_button.setEnabled(False)
        self.cancel_button.setEnabled(True)
        
        # Start the scanning process in a separate thread
        self.is_scanning = True
        threading.Thread(target=self.run_clamscan, args=(directory,)).start()

    def run_clamscan(self, directory):
        self.comm.update_display.emit("Scan in Progress...")
        
        try:
            # Run clamscan as a subprocess
            self.scan_process = subprocess.Popen(
                ["clamscan", "-r", directory],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Capture output line by line
            for line in iter(self.scan_process.stdout.readline, ''):
                if not self.is_scanning:
                    break
                self.comm.update_display.emit(line.strip())
                
                # Check if the line contains the infected file
                if "INFECTION" in line:
                    self.infected_files.append(line.strip())
            
            # Wait for the process to complete
            self.scan_process.wait()
            
            if self.is_scanning:  # If scan completed normally
                self.comm.update_display.emit("Scan completed successfully.\n")
            else:  # If scan was canceled
                self.comm.update_display.emit("Scan canceled by user.")
        
        except FileNotFoundError:
            self.comm.update_display.emit("Error: ClamAV (clamscan) not found.")
        except Exception as e:
            self.comm.update_display.emit(f"An unexpected error occurred: {e}")
        finally:
            self.finish_scan()

    def cancel_scan(self):
        if self.is_scanning and self.scan_process:
            self.comm.update_display.emit("Cancelling scan...")
            self.is_scanning = False
            self.scan_process.terminate()  # Terminate the scanning process

    def finish_scan(self):
        self.scan_process = None
        self.is_scanning = False
        # Re-enable scan buttons and disable cancel button
        self.scan_button.setEnabled(True)
        self.custom_scan_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        self.comm.update_display.emit("Scan Finished.")
        
        # Show the scan summary in a popup (message box)
        self.show_scan_summary()

    def show_scan_summary(self):
        # Create a summary message
        summary_message = "Scan Finished!\n"
        
        if self.infected_files:
            summary_message += f"Found {len(self.infected_files)} infected files:\n"
            for infected_file in self.infected_files:
                summary_message += f"- {infected_file}\n"
        else:
            summary_message += "No infected files found."
        
        # Display the summary in a message box (popup)
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setWindowTitle("Scan Summary")
        msg.setText(summary_message)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

# Main Application
app = QApplication(sys.argv)
window = ClamAVScanner()
window.show()
sys.exit(app.exec_())
