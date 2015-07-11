import socket
import traceback
import sys
import time
import threading
from core.ClientConnection import ChatClient, TransferClient
from core.ServerConnection import TransferServer, ChatServer

"""This module takes care of the server-client handshake business logic."""

class Handshake:
    
    """Initializes either the server or the client depending on mode"""
    
    def __init__(self, ip, channel, mode, callbacks):
        self.ip = ip
        self.channel = channel
        self.mode = mode
        self.callbacks = callbacks

    def start(self):
        listener = BroadcastListener(self.ip, self.channel)
        listener.start()

        is_server = listener.is_server

        if is_server:
            ip = self.ip
            channel = self.channel
            mode = self.mode
            callbacks = self.callbacks
            broadcaster = ServerBroadcast(ip, channel, mode, callbacks)
            broadcaster.start()
        else:
            if self.mode == 'chat':
                ip = listener.server_ip
                client_connection = ChatClient(ip, self.ip, self.callbacks)
            elif self.mode == 'transfer':
                ip = listener.server_ip
                client_connection = TransferClient(ip, self.ip, self.callbacks)

            client_connection.start()


class ServerBroadcast:
    
    """Takes care of UDP broadcasts to the whole network."""
    
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

        conn = self.server_connection
        if conn is not None and conn.is_connected:
            self.timer.cancel()

    def init_server(self):
        if self.mode == 'transfer':
            ip = self.server_ip
            self.server_connection = TransferServer(ip, self.callbacks)
        elif self.mode == 'chat':
            self.server_connection = ChatServer(self.server_ip, self.callbacks)

        self.server_connection.start()


class BroadcastListener:

    """Listens to the broadcasts emmited from ServerBroadcast and initializes TCP connection"""
    
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
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
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
