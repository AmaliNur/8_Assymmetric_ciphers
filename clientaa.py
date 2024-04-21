from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import socket
from key_manager import load_keys, serialize_public_key, deserialize_public_key

HOST = '127.0.0.1'
PORT = 8080

# Загрузка ключей
public_key, private_key = load_keys()

# Отправляем открытый ключ на сервер
with socket.socket() as sock:
    sock.connect((HOST, PORT))
    sock.send(serialize_public_key(public_key))

    # Принимаем открытый ключ сервера
    msg = sock.recv(1024)
    server_public_key = deserialize_public_key(msg)

    # Шифруем сообщение
    message = "Секретное сообщение"
    encrypted = server_public_key.encrypt(message.encode(), padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    sock.send(encrypted)

    # Принимаем ответ от сервера
    encrypted_response = sock.recv(1024)
    response = private_key.decrypt(encrypted_response, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)).decode()
    print("Ответ:", response)
