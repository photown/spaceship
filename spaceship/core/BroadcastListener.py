import socket
import traceback
from core import ClientConnection
import sys
import time

class BroadcastListener:

    def __init__(self, client_ip, channel):

        self.client_ip = client_ip
        self.channel = channel
        self.timeout_seconds = 1
        self.start_time = time.time()

    def start(self):

        current_time = time.time()
        if current_time - self.start_time > self.timeout_seconds:
            return

        host = '255.255.255.255'
        port = 8089

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.settimeout(self.timeout_seconds)
        self.sock.bind((host, port))

        self.listen_to_broadcast()

    def listen_to_broadcast(self):
        try:
            self.is_server = True
            message = None
            server_ip = None

            try:
                message, server_ip = self.sock.recvfrom(128)
            except KeyboardInterrupt:
                self.sock.close()
                return

            if message.decode() == self.channel:
                self.is_server = False
                self.server_ip = server_ip[0]
                self.sock.sendto(self.channel.encode(), server_ip)
            else:
                self.start()

            self.sock.close()
        except socket.timeout:
            pass