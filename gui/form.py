from typing import TYPE_CHECKING

from PyQt5.QtWidgets import *

from gui.form_ui import Ui_Form

if TYPE_CHECKING:
    from main.mainwindow import MainWindow


class FormWidget(Ui_Form, QWidget):

    def __init__(self, parent: "MainWindow"):
        super().__init__(parent=parent)
        self.setMinimumSize(400, 400)
        self.setupUi(self)

        print("hello")
