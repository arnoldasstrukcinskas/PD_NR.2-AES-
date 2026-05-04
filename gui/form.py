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

        self.cypherModeComboBox.currentTextChanged.connect(self.set_mode)
        self.bits128RadioButton.clicked.connect(self.set_bit_128_bits)
        self.bits192RadioButton.clicked.connect(self.set_bit_192_bits)
        self.bits256RadioButton.clicked.connect(self.set_bit_256_bits)

        self.keyTextEdit.textChanged.connect(self.set_key)
        self.inputTextEdit.textChanged.connect(self.set_text)

        self.cypherPushButton.clicked.connect(self.cypher)
        self.decypherPushButton.clicked.connect(self.decypher)

    def cypher(self):
        if self.cypherModeComboBox.currentIndex == 0:
            QMessageBox.critical(self, "Mode Error", "Select mode")

        if self.encryptor.key == "" or self.encryptor.key is None:
            QMessageBox.critical(self, "Key Error", "Missing key")

        if self.encryptor.text == "" or self.encryptor.text is None:
            QMessageBox.critical(self, "Text Error", "Missing text")

        self.inputTextEdit.setPlainText(self.encryptor.text)
        self.encryptor.cypher()
        self.resultTextEdit.setPlainText(self.encryptor.cyphered.hex())

    def decypher(self):
        if self.encryptor.key == "" or self.encryptor.key is None:
            QMessageBox.critical(self, "Key Error", "Missing key")

        if self.encryptor.cyphered is None:
            QMessageBox.critical(self, "Text Error", "Missing text")

        text = self.encryptor.decypher()

        self.inputTextEdit.setPlainText(self.encryptor.cyphered.hex())
        self.resultTextEdit.setPlainText(text)

    def set_mode(self, mode: str):
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
        self.encryptor.write_to_txt()

    def open_txt(self):
        self.encryptor.read_from_txt()
        self.cypherModeComboBox.setCurrentText(self.encryptor.mode)
        self.set_bits()
        self.keyTextEdit.setPlainText(self.encryptor.key)
        self.inputTextEdit.setPlainText(self.encryptor.cyphered.hex())

        self.decypher()

    def set_bits(self):
        if self.encryptor.bits == 128:
            self.bits128RadioButton.setChecked(True)
        elif self.encryptor.bits == 192:
            self.bits192RadioButton.setChecked(True)
        elif self.encryptor.bits == 256:
            self.bits256RadioButton.setChecked(True)
