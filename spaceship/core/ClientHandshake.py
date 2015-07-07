import socket
import traceback
from core import ClientConnection
import sys

class ClientHandshake:

    def __init__(self, client_ip):
        self.client_ip = client_ip

    def start(self):
        host = '255.255.255.255'
        port = 8089

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((host, port))

        self.listen_to_broadcast()

    def listen_to_broadcast(self):

        while 1:
            try:
                message, server_ip = self.sock.recvfrom(128)
                if message.decode() == 'First pass':
                    self.sock.sendto("I am here".encode(), server_ip)
                elif message.decode() == 'Second pass':
                    self.sock.close()
                    self.init_client(server_ip)
                    break

            except (KeyboardInterrupt, SystemExit):
                raise
            except:
                traceback.print_exc()
                break

    def init_client(self, server_ip):
        self.client_connection = ClientConnection.ClientConnection(server_ip, self.client_ip)
        self.client_connection.start()