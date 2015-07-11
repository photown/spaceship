import socket
import threading
from core.ServerConnection import ServerConnection

class ServerBroadcast:

    def __init__(self, server_ip, channel, mode, callbacks):
        self.server_ip = server_ip
        self.channel = channel
        self.server_connection = None
        self.mode = mode
        self.callbacks = callbacks

    def start(self):
        self.setup_socket()
        self.init_server()

    def setup_socket(self):
        self.cs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.cs.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.cs.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.cs.bind((self.server_ip, 8089))

        self.ping_broadcast()

    def ping_broadcast(self):
        self.cs.sendto(self.channel.encode(), ('255.255.255.255', 8089))
        self.timer = threading.Timer(1, self.ping_broadcast)
        self.timer.start()

        if not self.server_connection is None and self.server_connection.is_connected:
            self.timer.cancel()

    def init_server(self):
        self.server_connection = ServerConnection(self.server_ip, self.mode, self.callbacks)
        self.server_connection.start()