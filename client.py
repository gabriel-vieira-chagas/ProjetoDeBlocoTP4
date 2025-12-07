import socket
import threading
import sys

nickname = input("Escolha seu apelido: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    client.connect(('127.0.0.1', 55555))
except ConnectionRefusedError:
    print("Não foi possível conectar ao servidor. Verifique se ele está ligado.")
    sys.exit()


def receive():
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            if message == 'NICK':
                client.send(nickname.encode('utf-8'))
            else:
                print(message)
        except:
            print("Ocorreu um erro! Conexão encerrada.")
            client.close()
            break


def write():
    while True:
        try:
            text = input("")
            if text.lower() == 'sair':
                client.close()
                break

            message = f'{nickname}: {text}'
            client.send(message.encode('utf-8'))
        except:
            break

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()