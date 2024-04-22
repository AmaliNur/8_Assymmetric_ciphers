import socket
import pickle
from crypto_utils import load_keys, serialize_public_key, rsa_encrypt

# Загрузка ключей
public_key, private_key = load_keys()

HOST = '127.0.0.1'
PORT = 8080

# Отправляем открытый ключ на сервер
with socket.socket() as sock:
    sock.connect((HOST, PORT))
    sock.send(serialize_public_key(public_key))

    # Шифруем сообщение
    message = "Секретное сообщение"
    encrypted = rsa_encrypt(message, public_key)
    sock.send(encrypted)

    # Принимаем ответ от сервера
    response = sock.recv(1024)
    print("Ответ от сервера:", response.decode())
