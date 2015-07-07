import socket
import sys

class ServerConnection:
    def __init__(self, server_ip):
        self.server_ip = server_ip
        self.is_connected = False

    def start(self):
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serversocket.bind((self.server_ip, 8087))
        self.serversocket.listen(5)

        connection, address = self.serversocket.accept()
        self.is_connected = True

        sys.stdin = sys.stdin.detach();
        while True:
            data = sys.stdin.read(128)
            connection.send(data)
            if not data:
                connection.close()
                self.serversocket.close()
                break

