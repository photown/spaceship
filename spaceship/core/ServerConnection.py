import socket
import sys
from threading import Thread
import getpass
import os

class ServerConnection:
    def __init__(self, server_ip, mode, callbacks):
        self.server_ip = server_ip
        self.is_connected = False
        self.mode = mode

        if mode == 'chat':
            self.ready_for_chat, self.on_send, self.on_receive = callbacks
        elif mode == 'transfer':
            self.transfer_send, self.transfer_receive = callbacks

    def start(self):
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serversocket.bind((self.server_ip, 8087))
        self.serversocket.listen(5)

        connection = None
        address = None

        try:
            connection, address = self.serversocket.accept()
        except KeyboardInterrupt:
            self.serversocket.close()
            os.kill(os.getpid(), 1)
            return

        self.is_connected = True
        self.connection = connection

        if self.mode == 'transfer':
            self.transfer_send(self.stream_buffer)
        elif self.mode == 'chat':
            self.thread = Thread(target = self.printer)
            self.thread.daemon = True
            self.thread.start()

            self.ready_for_chat(self.send_message)
    
    def stream_buffer(self, stream_buffer):
        while True:
            data = stream_buffer.read(128)
            if data:
                self.connection.send(data)
            else:
                self.connection.close()
                self.serversocket.close()
                break

    def send_message(self, message):
        self.connection.send(message.encode())
        self.on_send(message)

    def printer(self):
        while True:
            buf = self.connection.recv(128)
            if len(buf) > 0:
                self.on_receive(getpass.getuser(), self.server_ip, buf.decode())

