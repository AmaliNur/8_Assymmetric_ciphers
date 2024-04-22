import socket
import pickle
from crypto_utils import load_keys, serialize_public_key, rsa_encrypt

# Загрузка ключей
public_key, private_key = load_keys()

HOST = '127.0.0.1'
PORT_KEY_EXCHANGE = 8080
PORT_COMMUNICATION = 8081

# Подключаемся для установки режима шифрования
with socket.socket() as key_exchange_sock:
    key_exchange_sock.connect((HOST, PORT_KEY_EXCHANGE))
    key_exchange_sock.send(serialize_public_key(public_key))

    # Шифруем порт для основного общения
    encrypted_port = rsa_encrypt(str(PORT_COMMUNICATION), public_key)
    key_exchange_sock.send(encrypted_port)

# Основное общение на другом порту
with socket.socket() as communication_sock:
    communication_sock.connect((HOST, PORT_COMMUNICATION))

    # Шифруем и отправляем сообщение
    message = "Секретное сообщение"
    encrypted = rsa_encrypt(message, public_key)
    communication_sock.send(encrypted)

    # Принимаем ответ от сервера
    response = communication_sock.recv(1024)
    print("Ответ от сервера:", response.decode())
