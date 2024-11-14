import sys
import pyclamd
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QRadioButton, QMessageBox, QHBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal, QTimer
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import concurrent.futures
import os

# Check ClamD connection on initialization
try:
    cd = pyclamd.ClamdUnixSocket()
    if not cd.ping():
        raise ConnectionError("Unable to connect to ClamD service.")
except Exception as e:
    print("Error connecting to ClamD:", e)
    sys.exit(1)

class FileEventHandler(FileSystemEventHandler):
    """Custom handler for file system events."""
    def __init__(self, scan_callback):
        super().__init__()
        self.scan_callback = scan_callback

    def on_created(self, event):
        # Scan only folders or .txt files
        if event.is_directory or event.src_path.endswith('.txt'):
            print(f"Created: {event.src_path}")  # Debug: Log created files/folders
            self.scan_callback(event.src_path)

class RealTimeScanner(QThread):
    """Thread that handles real-time scanning using Watchdog."""
    file_detected = pyqtSignal(str)  # Signal to emit if malware is found
    status_update = pyqtSignal(str)  # Signal to update status in GUI
    process_batch_signal = pyqtSignal()  # Signal to trigger batch processing in main thread
    scan_batch = []  # Collect files to scan in batch

    def __init__(self, folder_to_watch):
        super().__init__()
        self.folder_to_watch = folder_to_watch
        self.observer = Observer()
        self.handler = FileEventHandler(scan_callback=self.scan_file)
        self.running = False
        self.executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)  # Thread pool for scanning

        # Connect signal to batch processing method
        self.process_batch_signal.connect(self.process_scan_batch)

    def run(self):
        """Start the file observer for real-time scanning."""
        print(f"Starting observer on {self.folder_to_watch}")  # Debug: Ensure observer starts
        self.observer.schedule(self.handler, self.folder_to_watch, recursive=True)
        self.observer.start()
        self.running = True
        self.status_update.emit("Real-time protection: ON")
        try:
            while self.running:
                self.observer.join(1)
        finally:
            self.status_update.emit("Real-time protection: OFF")

    def stop(self):
        """Stop the file observer and reset status."""
        self.running = False
        self.observer.stop()
        self.observer.join()

    def scan_file(self, file_path):
        """Add file to the scan batch to avoid immediate scanning."""
        print(f"File to scan: {file_path}")  # Debug: Log files to scan
        if file_path not in self.scan_batch:
            self.scan_batch.append(file_path)
        
        # Trigger batch processing in the main thread after a delay
        self.process_batch_signal.emit()

    def process_scan_batch(self):
        """Process the batch of files."""
        if not self.scan_batch:
            return
        
        # Update status to show batch scanning started
        self.status_update.emit("Batch scanning started...")

        # Scan files in parallel using the thread pool
        futures = [self.executor.submit(self.scan_single_file, file) for file in self.scan_batch]
        for future in concurrent.futures.as_completed(futures):
            future.result()  # Wait for all futures to complete
        
        # After scanning batch, update status
        self.status_update.emit(f"Scanned {len(self.scan_batch)} files.")
        
        self.scan_batch.clear()  # Clear the batch after scanning

    def scan_single_file(self, file_path):
        """Scan a single file or folder."""
        print(f"Scanning file/folder: {file_path}")  # Debug: Log scanning start
        self.status_update.emit(f"Scanning: {file_path}")
        
        try:
            result = cd.scan_file(file_path)
            
            if result:
                # If result is not None, the file is either clean or infected
                for file, result in result.items():
                    # Check if the file is infected
                    if result == 'OK':
                        message = f"No malware found in: {file_path}"
                    else:
                        message = f"Malware detected in: {file_path} - {result}"
                    
                    self.file_detected.emit(message)
                    
            else:
                # If ClamAV doesn't return anything, then file is likely clean
                message = f"No malware found in: {file_path}"
                self.file_detected.emit(message)

        except Exception as e:
            print(f"Error scanning file {file_path}: {e}")
            self.file_detected.emit(f"Error scanning file {file_path}: {e}")


class RealTimeProtectionApp(QWidget):
    """Main application GUI for real-time protection control."""
    def __init__(self):
        super().__init__()
        self.scanner_thread = None
        self.folder_to_watch = "/home/vimal/Desktop/"  # Update with desired directory to monitor
        self.initUI()

    def initUI(self):
        """Set up the GUI layout and elements."""
        self.setWindowTitle("Real-Time Protection")
        self.setGeometry(300, 300, 400, 200)

        # Layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Status Label
        self.status_label = QLabel("Real-time protection: OFF")
        layout.addWidget(self.status_label)

        # Protection Toggle Buttons
        toggle_layout = QHBoxLayout()
        self.radio_on = QRadioButton("On")
        self.radio_off = QRadioButton("Off")
        self.radio_off.setChecked(True)
        self.radio_on.toggled.connect(self.toggle_protection)
        toggle_layout.addWidget(self.radio_on)
        toggle_layout.addWidget(self.radio_off)
        layout.addLayout(toggle_layout)

    def toggle_protection(self):
        """Toggle protection on or off based on selected radio button."""
        if self.radio_on.isChecked():
            self.start_protection()
        else:
            self.stop_protection()

    def start_protection(self):
        """Start real-time protection with a background scanner thread."""
        if not self.scanner_thread:
            self.scanner_thread = RealTimeScanner(folder_to_watch=self.folder_to_watch)
            self.scanner_thread.file_detected.connect(self.show_alert)
            self.scanner_thread.status_update.connect(self.update_status)
            self.scanner_thread.start()
            QMessageBox.information(self, "Real-Time Protection", "Real-time protection is now ON.")

    def stop_protection(self):
        """Stop real-time protection by terminating the scanner thread."""
        if self.scanner_thread:
            self.scanner_thread.stop()
            self.scanner_thread.wait()
            self.scanner_thread = None
            self.update_status("Real-time protection: OFF")
            QMessageBox.information(self, "Real-Time Protection", "Real-time protection is now OFF.")

    def update_status(self, message):
        """Update status label with current activity."""
        self.status_label.setText(message)

    def show_alert(self, message):
        """Show alert message when malware is detected or when scan is complete."""
        QMessageBox.warning(self, "Scan Result", message)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RealTimeProtectionApp()
    window.show()
    sys.exit(app.exec_())
