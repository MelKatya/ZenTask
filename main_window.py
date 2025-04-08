import sys
from PySide6.QtWidgets import QApplication, QWidget, QDialog, QMainWindow
from forms.ui_main_form import MainForm
import utils


class MainWindow(MainForm):
    def __init__(self):
        super().__init__()


        self.pushButton_nt_my_task.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.pushButton_nt_not.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))

