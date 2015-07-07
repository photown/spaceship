import socket
import time, threading, traceback
from core import ServerConnection
import sys

class ServerHandshake:

    def __init__(self, server_ip):
        self.server_ip = server_ip

    def start(self):
        self.cs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.cs.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.cs.bind((self.server_ip, 8089))

        self.ping_broadcast()
        self.listen_for_ping_answer()

    def ping_broadcast(self):
        self.cs.sendto('First pass'.encode(), ('255.255.255.255', 8089))
        self.timer = threading.Timer(1, self.ping_broadcast)
        self.timer.start()

    def listen_for_ping_answer(self):
        try:
            message, client_ip = self.cs.recvfrom(128)
            self.timer.cancel()
            
            self.send_affirmation_to_client()
            self.init_server(client_ip)
        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            traceback.print_exc()
        finally:
            self.cs.close()

    def send_affirmation_to_client(self):
        self.cs.sendto('Second pass'.encode(), ('255.255.255.255', 8089))

    def init_server(self, client_ip):
        self.server_connection = ServerConnection.ServerConnection(self.server_ip, client_ip)
        self.server_connection.start()