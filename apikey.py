import os
import os.path as _path

import click
from cryptography.fernet import Fernet

key = ""
fernet = ""

ROOT_FOLDER: str = _path.join(_path.expanduser("~"), ".moviecli")
KEY_PATH: str = _path.join(ROOT_FOLDER, "key.txt")
API_PATH: str = _path.join(ROOT_FOLDER, "api.txt")


@click.command()
@click.argument("apikey")
def add_apikey(apikey: str) -> None:
    """Adds apikey to moviecli."""

    # creating folder in the system if it does not exist
    if not _path.exists(ROOT_FOLDER):
        os.makedirs(ROOT_FOLDER)

    # generate key for the encryption
    if not _path.isfile(KEY_PATH):
        global key
        global fernet
        key = Fernet.generate_key()
        fernet = Fernet(key=key)
        with open(KEY_PATH, "w") as keyFile:
            keyFile.write(key.decode())

    # encrypt the original api key
    encApi = fernet.encrypt(apikey.encode())

    with open(API_PATH, "w") as apiFile:
        apiFile.write(encApi.decode())

    click.echo("✨ Added Api Key to $HOME/.moviecli/api.txt")


def decrypt_key() -> str:
    """Decrepts key from the package root folder."""

    if not _path.isfile(KEY_PATH):
        raise Exception("⛔ Encryption key not found.")

    if not _path.isfile(API_PATH):
        raise Exception("⛔ API key not found.")

    with open(KEY_PATH, "r") as keyFile:
        key: str = keyFile.read().strip()

    fernet: Fernet = Fernet(key.encode())

    with open(API_PATH, "r") as apiFile:
        enckey: str = apiFile.readline().strip("\n")

    encApi: bytes = enckey.encode()
    original_apiKey: bytes = fernet.decrypt(encApi)

    return original_apiKey.decode()
