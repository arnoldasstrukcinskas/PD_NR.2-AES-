import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from gui.form import FormWidget
from main.mainwindow_ui import Ui_MainWindow


class MainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.formWidget = FormWidget(self)
        self.verticalLayout_2.addWidget(self.formWidget)
