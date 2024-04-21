from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
import socket
from key_manager import load_keys, serialize_public_key, deserialize_public_key

HOST = '127.0.0.1'
PORT = 8080

# Загрузка ключей
public_key, private_key = load_keys()

with socket.socket() as sock:
    sock.bind((HOST, PORT))
    sock.listen(1)
    conn, addr = sock.accept()

    # Принимаем открытый ключ клиента
    msg = conn.recv(1024)
    client_public_key = deserialize_public_key(msg)

    # Отправляем открытый ключ сервера
    conn.send(serialize_public_key(public_key))

    # Принимаем зашифрованное сообщение
    encrypted_message = conn.recv(1024)
    message = private_key.decrypt(encrypted_message, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)).decode()
    print("Получено сообщение:", message)

    # Отправляем ответ
    response = "Привет, клиент!"
    encrypted_response = client_public_key.encrypt(response.encode(), padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))
    conn.send(encrypted_response)
