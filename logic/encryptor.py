import os

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Util.Padding import pad, unpad
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMessageBox


class Encryptor(QObject):
    def __init__(self):
        super().__init__()
        print("encryptor started")
        self.text: str = None
        self.key: str = None
        self.mode: int = None
        self.bits: int = None
        self.iv: bytes = None
        self.generated_key: str = None

    def cypher(self):
        bytes = int(self.bits / 8)
        key = PBKDF2(self.key, "fixedSalt", dkLen=bytes, count=10000)
        iv = os.urandom(16)
        self.iv = iv
        self.generated_key = key
        if self.mode == 1:
            cipher = AES.new(key, AES.MODE_ECB)
        elif self.mode == 2:
            cipher = AES.new(key, AES.MODE_CBC, iv=iv)
            print(iv.hex())
        elif self.mode == 3:
            cipher = AES.new(key, AES.MODE_CFB, iv=iv)
        else:
            raise ValueError("Wrong mode")

        padded_text = pad(self.text.encode("utf-8"), 16, style="pkcs7")

        cyphered_text = cipher.encrypt(padded_text)
        self.cyphered = cyphered_text
        return cyphered_text

    def decypher(self):
        bytes = int(self.bits / 8)
        key = self.generated_key
        iv = self.iv
        decipher = None
        if self.mode == 1:
            decipher = AES.new(key, AES.MODE_ECB)
        elif self.mode == 2:
            decipher = AES.new(key, AES.MODE_CBC, iv=iv)
            print(iv.hex())
        elif self.mode == 3:
            decipher = AES.new(key, AES.MODE_CFB, iv=iv)
        else:
            raise ValueError("Wrong mode")

        decyphered_text = decipher.decrypt(self.cyphered)

        return unpad(decyphered_text, 16, style="pkcs7").decode("utf-8")

    def write_to_txt(self):
        print("writing to txt")

    def read_from_txt(self):
        print("reading from txt")
