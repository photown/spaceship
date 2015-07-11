import socket
import os
import getpass
from threading import Thread

"""This module taces care of the server-specific logic."""

class ServerConnection:

    """Base class which takes care of initializing the server endpoint for either chat or transfer."""

    def __init__(self, server_ip, callbacks):
        self.server_ip = server_ip
        self.is_connected = False

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

        self.write_to_client()


class ChatServer(ServerConnection):

    """Takes care of initializing the server endpoint for chat."""

    def __init__(self, server_ip, callbacks):
        ServerConnection.__init__(self, server_ip, callbacks)
        self.ready_for_chat, self.on_send, self.on_receive = callbacks

    def write_to_client(self):
        self.thread = Thread(target=self.printer)
        self.thread.daemon = True
        self.thread.start()

        self.ready_for_chat(self.send_message)

    def send_message(self, message):
        self.connection.send(message.encode())
        self.on_send(message)

    def printer(self):
        while True:
            buf = self.connection.recv(128)
            if len(buf) > 0:
                user = getpass.getuser()
                self.on_receive(user, self.server_ip, buf.decode())


class TransferServer(ServerConnection):

    """Takes care of initializing the server endpoint for transfer."""

    def __init__(self, server_ip, callbacks):
        ServerConnection.__init__(self, server_ip, callbacks)
        self.transfer_send, self.transfer_receive = callbacks

    def write_to_client(self):
        self.transfer_send(self.stream_buffer)

    def stream_buffer(self, stream_buffer):
        while True:
            data = stream_buffer.read(128)
            if data:
                self.connection.send(data)
            else:
                self.connection.close()
                self.serversocket.close()
                break
