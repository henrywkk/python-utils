import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class Crypt(object):

    @staticmethod
    def getfenet(master_key: str) -> Fernet:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=b'QlpoOTFBWSZTW',
            iterations=100000,
            backend=default_backend(),
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_key.encode('utf-8')))
        return Fernet(key)

    @staticmethod
    def encode(value: str, master_key: str) -> str:
        f = Crypt.getfenet(master_key)
        return f.encrypt(value.encode('utf-8')).decode('utf-8')

    @staticmethod
    def decode(value: str, master_key: str) -> str:
        f = Crypt.getfenet(master_key)
        return f.decrypt(value.encode('utf-8')).decode('utf-8')


if __name__ == "__main__":
    my_master_key = "simple_master_key"
    password_value = "P@ss1234"
    token = Crypt.encode(password_value, my_master_key)
    print(token)
    revert = Crypt.decode(token, my_master_key)
    print(revert)
