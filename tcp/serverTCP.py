import socket
import sys

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

serverPort = 6789
serverIP = "192.168.0.48"
serverSocket.bind((serverIP, serverPort))
serverSocket.listen(1)

try:
    while True:
        print('Servidor rodando...')
        connectionSocket, addr = serverSocket.accept()

        try:
            message = connectionSocket.recv(1024).decode()
            message_parts = message.split()

            if len(message_parts) < 2:
                raise ValueError("Requisição HTTP inválida")

            filename = message_parts[1][1:]
            f = open(filename)
            outputdata = f.read()
            connectionSocket.send("HTTP/1.1 200 OK\r\n\r\n".encode())
            connectionSocket.sendall(outputdata.encode())
        except (IOError, ValueError):
            connectionSocket.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
        finally:
            connectionSocket.close()
except KeyboardInterrupt:
    print("\nEncerrando o servidor...")
    serverSocket.close()
    sys.exit(0)
