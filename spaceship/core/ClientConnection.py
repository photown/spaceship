import socket
import sys

class ClientConnection:
    def __init__(self, server_ip, client_ip):
        self.server_ip = server_ip
        self.client_ip = client_ip

    def start(self):
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientsocket.connect((self.server_ip, 8087))

        self.read_from_server()

    def read_from_server(self):
        while True:
            buf = self.clientsocket.recv(128)
            if len(buf) > 0:
                sys.stdout.buffer.write(buf)
            else:
                break
        self.clientsocket.close()