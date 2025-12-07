import socket
import threading

# Configurações de conexão
HOST = '127.0.0.1'  # Localhost
PORT = 55555        # Porta arbitrária (acima de 1024)

# Iniciando o servidor
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            pass

def handle(client):
    while True:
        try:
            # Recebe mensagem do cliente
            message = client.recv(1024)
            broadcast(message)
        except:
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                broadcast(f'{nickname} saiu do chat!'.encode('utf-8'))
                nicknames.remove(nickname)
                break

def receive():
    print(f"Servidor ouvindo em {HOST}:{PORT}...")
    while True:
        client, address = server.accept()
        print(f"Conectado com {str(address)}")

        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f"Apelido do cliente é {nickname}")
        broadcast(f"{nickname} entrou no chat!".encode('utf-8'))
        client.send('Conectado ao servidor!'.encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

if __name__ == "__main__":
    receive()