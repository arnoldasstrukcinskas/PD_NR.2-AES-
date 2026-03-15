from typing import TYPE_CHECKING

from PyQt5.QtWidgets import *

from gui.form_ui import Ui_Form
from logic.encryptor import Encryptor

if TYPE_CHECKING:
    from main.mainwindow import MainWindow

BITS128 = 128
BITS192 = 192
BITS256 = 256


class FormWidget(Ui_Form, QWidget):

    def __init__(self, parent: "MainWindow"):
        super().__init__(parent=parent)
        self.setMinimumSize(400, 400)
        self.setupUi(self)
        self.encryptor = Encryptor()

        self.cypherModeComboBox.currentIndexChanged.connect(self.set_mode)
        self.bits128RadioButton.clicked.connect(self.set_bit_128_bits)
        self.bits192RadioButton.clicked.connect(self.set_bit_192_bits)
        self.bits256RadioButton.clicked.connect(self.set_bit_256_bits)

        self.keyTextEdit.textChanged.connect(self.set_key)
        self.inputTextEdit.textChanged.connect(self.set_text)

        self.cypherPushButton.clicked.connect(self.cypher)
        self.decypherPushButton.clicked.connect(self.decypher)

    def cypher(self):
        if self.encryptor.key == "" or self.encryptor.key is None:
            QMessageBox.critical(self, "Key Error", "Missing key")

        if self.encryptor.text == "" or self.encryptor.text is None:
            QMessageBox.critical(self, "Text Error", "Missing text")

        self.inputTextEdit.setPlainText(self.encryptor.text)
        text = self.encryptor.cypher().hex()
        self.resultTextEdit.setPlainText(text)

    def decypher(self):
        if self.encryptor.key == "" or self.encryptor.key is None:
            QMessageBox.critical(self, "Key Error", "Missing key")

        if self.encryptor.text == "" or self.encryptor.text is None:
            QMessageBox.critical(self, "Text Error", "Missing text")

        text = self.encryptor.decypher()

        self.inputTextEdit.setPlainText(self.encryptor.text)
        self.resultTextEdit.setPlainText(text)

    def set_mode(self, mode: int):
        self.encryptor.mode = mode

    def set_bit_128_bits(self):
        self.encryptor.bits = BITS128

    def set_bit_192_bits(self):
        self.encryptor.bits = BITS192

    def set_bit_256_bits(self):
        self.encryptor.bits = BITS256

    def set_text(self):
        self.encryptor.text = self.inputTextEdit.toPlainText()

    def set_key(self):
        self.encryptor.key = self.keyTextEdit.toPlainText()

    def save_to_txt(self):
        print("Saved to txt")

    def open_txt(self):
        print("Opened txt")
