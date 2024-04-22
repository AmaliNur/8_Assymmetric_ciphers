import socket
import pickle
from crypto_utils import load_keys, deserialize_public_key, rsa_decrypt

# Загрузка ключей
public_key, private_key = load_keys()

def check_client_key(client_key):
    return client_key == public_key

HOST = '127.0.0.1'
PORT_KEY_EXCHANGE = 8080
PORT_COMMUNICATION = 8081

with socket.socket() as key_exchange_sock:
    key_exchange_sock.bind((HOST, PORT_KEY_EXCHANGE))
    key_exchange_sock.listen(1)
    conn, addr = key_exchange_sock.accept()

    # Принимаем открытый ключ клиента
    msg = conn.recv(1024)
    client_public_key = deserialize_public_key(msg)

    # Проверяем ключ клиента
    if not check_client_key(client_public_key):
        print("Недопустимый ключ клиента. Разрыв соединения.")
        conn.close()
    else:
        print("Ключ клиента допустим. Продолжаем соединение.")

        # Принимаем зашифрованный порт
        encrypted_port = conn.recv(1024)
        port = int(rsa_decrypt(encrypted_port, private_key))

# Теперь слушаем соединения на порту для основного общения
with socket.socket() as communication_sock:
    communication_sock.bind((HOST, port))
    communication_sock.listen(1)
    conn, addr = communication_sock.accept()

    # Принимаем зашифрованное сообщение
    encrypted_message = conn.recv(1024)
    message = rsa_decrypt(encrypted_message, private_key)
    print("Получено сообщение:", message)

    # Отправляем ответ
    response = "Привет, клиент!"
    conn.send(response.encode())
