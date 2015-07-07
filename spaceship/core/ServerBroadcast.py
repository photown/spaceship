import socket
import time, threading, traceback
from core import ServerConnection
import sys

class ServerBroadcast:

    def __init__(self, server_ip):
        self.server_ip = server_ip

    def start(self):
        self.cs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.cs.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.cs.bind((self.server_ip, 8089))

        self.ping_broadcast()
        self.init_server()

    def ping_broadcast(self):
        self.cs.sendto('kittens'.encode(), ('255.255.255.255', 8089))
        self.timer = threading.Timer(1, self.ping_broadcast)
        self.timer.start()

    def init_server(self):
        self.server_connection = ServerConnection.ServerConnection(self.server_ip)
        self.server_connection.start()