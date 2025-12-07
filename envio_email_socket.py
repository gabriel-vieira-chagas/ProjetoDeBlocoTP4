import socket

def main():
    destinatario = input("Digite o e-mail do destinatário: ")
    assunto = input("Digite o título do e-mail: ")
    corpo = input("Digite o conteúdo da mensagem: ")

    server_host = 'localhost'
    server_port = 1025
    sender_email = "aluno@infnet.edu.br"

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((server_host, server_port))
        client_socket.recv(1024)

        cmd_helo = 'HELO cliente\r\n'
        client_socket.send(cmd_helo.encode())
        client_socket.recv(1024)

        cmd_mail_from = f'MAIL FROM: <{sender_email}>\r\n'
        client_socket.send(cmd_mail_from.encode())
        client_socket.recv(1024)

        cmd_rcpt_to = f'RCPT TO: <{destinatario}>\r\n'
        client_socket.send(cmd_rcpt_to.encode())
        client_socket.recv(1024)

        cmd_data = 'DATA\r\n'
        client_socket.send(cmd_data.encode())
        client_socket.recv(1024)

        mensagem_formatada = f"Subject: {assunto}\nFrom: {sender_email}\nTo: {destinatario}\n\n{corpo}\r\n.\r\n"
        client_socket.send(mensagem_formatada.encode())
        resposta_final = client_socket.recv(1024).decode()

        if '250' in resposta_final:
            print("E-mail enviado com sucesso.")
        else:
            print(f"Erro ao enviar: {resposta_final}")

        client_socket.send('QUIT\r\n'.encode())
        client_socket.close()

    except Exception as e:
        print(f"Ocorreu um erro na conexão: {e}")

if __name__ == "__main__":
    main()