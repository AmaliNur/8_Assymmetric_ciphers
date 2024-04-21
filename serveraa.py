import socket
import pickle
from crypto_utils import generate_rsa_keys, serialize_public_key, deserialize_public_key, rsa_encrypt, rsa_decrypt

HOST = '127.0.0.1'
PORT = 8080

# Генерируем ключи сервера
public_key, private_key = generate_rsa_keys()

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
    message = rsa_decrypt(encrypted_message, private_key)
    print("Получено сообщение:", message)

    # Отправляем ответ
    response = "Привет, клиент!"
    encrypted_response = rsa_encrypt(response, client_public_key)
    conn.send(encrypted_response)
