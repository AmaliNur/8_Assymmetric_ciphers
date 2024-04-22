import socket
import pickle
from crypto_utils import load_keys, deserialize_public_key, rsa_decrypt

# Загрузка ключей
public_key, private_key = load_keys()

def check_client_key(client_key):
    return client_key == public_key

HOST = '127.0.0.1'
PORT = 8080

with socket.socket() as sock:
    sock.bind((HOST, PORT))
    sock.listen(1)
    conn, addr = sock.accept()

    # Принимаем открытый ключ клиента
    msg = conn.recv(1024)
    client_public_key = deserialize_public_key(msg)

    # Проверяем ключ клиента
    if not check_client_key(client_public_key):
        print("Недопустимый ключ клиента. Разрыв соединения.")
        conn.close()
    else:
        print("Ключ клиента допустим. Продолжаем соединение.")

        # Принимаем зашифрованное сообщение
        encrypted_message = conn.recv(1024)
        message = rsa_decrypt(encrypted_message, private_key)
        print("Получено сообщение:", message)

        # Отправляем ответ
        response = "Привет, клиент!"
        conn.send(response.encode())