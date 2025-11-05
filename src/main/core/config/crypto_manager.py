import cryptography
from cryptography.fernet import Fernet
import cryptography.fernet
import keyring

MY_APP = "db_catcher"
KEY_NAME = "credential_key"

def verifyKey():
    if not keyring.get_password(MY_APP, KEY_NAME):
        new_key = Fernet.generate_key().decode()
        keyring.set_password(MY_APP, KEY_NAME, new_key)

def encrypt(value: str) -> str:
    verifyKey()
    pwd = keyring.get_password(MY_APP, KEY_NAME)
    assert pwd
    key = pwd.encode()
    fernet = Fernet(key)

    return fernet.encrypt(value.encode()).decode()

def decrypt(value: str) -> str:
    pwd = keyring.get_password(MY_APP, KEY_NAME)
    assert pwd
    key = pwd.encode()
    fernet = Fernet(key)
    try:
        plain = fernet.decrypt(value).decode()
        return plain
    except cryptography.fernet.InvalidToken as e:
        return value
