import socket
import traceback
from core import ClientConnection
import sys

class BroadcastListener:

    def __init__(self, client_ip):
        self.client_ip = client_ip
        self.timeout_seconds = 1

    def start(self):
        host = '255.255.255.255'
        port = 8089

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(self.timeout_seconds)
        self.sock.bind((host, port))

        self.listen_to_broadcast()

    def listen_to_broadcast(self):
        try:
            self.is_server = True
            message, server_ip = self.sock.recvfrom(128)
            self.is_server = False
            self.server_ip = server_ip[0]
            self.sock.sendto("I am here".encode(), server_ip)
            self.sock.close()
        except socket.timeout:
            pass

    def init_client(self, server_ip):
        self.client_connection = ClientConnection.ClientConnection(server_ip, self.client_ip)
        self.client_connection.start()