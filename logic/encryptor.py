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
        self.mode: str = None
        self.bits: int = None
        self.iv: bytes = None
        self.generated_key: str = None
        self.data: dict = {}
        self.save_dir: str = "data"
        self.cyphered: bytes = None

    def cypher(self):
        bytes = int(self.bits / 8)
        key = PBKDF2(self.key, "fixedSalt", dkLen=bytes, count=10000)
        iv = os.urandom(16)
        self.iv = iv
        self.generated_key = key
        if self.mode == "ECB":
            cipher = AES.new(key, AES.MODE_ECB)
            padded_text = pad(self.text.encode("utf-8"), 16, style="pkcs7")
        elif self.mode == "CBC":
            cipher = AES.new(key, AES.MODE_CBC, iv=iv)
            padded_text = pad(self.text.encode("utf-8"), 16, style="pkcs7")
            # print(iv.hex())
        elif self.mode == "CFB":
            cipher = AES.new(key, AES.MODE_CFB, iv=iv)
            padded_text = self.text.encode("utf-8")
        else:
            raise ValueError("Wrong mode")

        cyphered_text = cipher.encrypt(padded_text)

        self.cyphered = cyphered_text

        # Fill data dict for saving
        self.data["key"] = self.key
        self.data["iv"] = iv.hex()
        self.data["mode"] = self.mode
        self.data["bits"] = self.bits
        self.data["cyphered_text"] = self.cyphered.hex()

    def decypher(self):
        counted_bytes = int(self.bits / 8)
        key = PBKDF2(self.key, "fixedSalt", dkLen=counted_bytes, count=10000)

        decipher = None
        if self.mode == "ECB":
            decipher = AES.new(key, AES.MODE_ECB)
        elif self.mode == "CBC":
            decipher = AES.new(key, AES.MODE_CBC, iv=self.iv)
        elif self.mode == "CFB":
            decipher = AES.new(key, AES.MODE_CFB, iv=self.iv)
        else:
            raise ValueError("Wrong mode")

        cyphered_text = self.cyphered

        decyphered_text = decipher.decrypt(cyphered_text)

        if not self.mode == "CFB":
            text = unpad(decyphered_text, 16, style="pkcs7").decode("utf-8")
        else:
            text = decyphered_text.decode("utf-8")

        print(text)
        return text

    def write_to_txt(self):
        os.makedirs(self.save_dir, exist_ok=True)

        file_path = os.path.join(self.save_dir, "saved.txt")

        with open(file_path, "w", encoding="utf-8") as f:
            for key, value in self.data.items():
                f.write(f"{key}: {value}\n")

    def read_from_txt(self):
        self.data = {}

        file_path = os.path.join("data/saved.txt")

        with open(file_path, "r", encoding="utf-8") as f:
            for row in f:
                key, value = row.strip().split(": ", 1)
                self.data[key] = value

        self.cyphered = bytes.fromhex(self.data["cyphered_text"])
        self.key = self.data["key"]
        self.iv = bytes.fromhex(self.data["iv"])
        self.mode = self.data["mode"]
        self.bits = int(self.data["bits"])
        # Ideti, kad kai atidaro, atnaujina UI.
