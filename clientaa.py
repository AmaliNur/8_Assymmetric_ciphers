import socket
from crypto_utils import generate_rsa_keys, serialize_public_key, deserialize_public_key, rsa_encrypt, rsa_decrypt

HOST = '127.0.0.1'
PORT = 8080

# Генерируем ключи клиента
public_key, private_key = generate_rsa_keys()

# Отправляем открытый ключ на сервер
with socket.socket() as sock:
    sock.connect((HOST, PORT))
    sock.send(serialize_public_key(public_key))

    # Принимаем открытый ключ сервера
    msg = sock.recv(1024)
    server_public_key = deserialize_public_key(msg)

    # Шифруем сообщение
    message = "Секретное сообщение"
    encrypted = rsa_encrypt(message, server_public_key)
    sock.send(encrypted)

    # Принимаем ответ от сервера
    encrypted_response = sock.recv(1024)
    response = rsa_decrypt(encrypted_response, private_key)
    print("Ответ:", response)
