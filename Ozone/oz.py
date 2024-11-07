import sys
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi

class MainWindow(QDialog):  # Change QMainWindow to QDialog
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("MainPage.ui", self)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())
