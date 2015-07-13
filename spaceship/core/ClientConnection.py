import socket
import getpass
from threading import Thread

"""This module taces care of the server-specific logic."""


class ClientConnection:

    """Base class which takes care of initializing the client \
    for either chat or transfer."""

    def __init__(self, server_ip, client_ip, callbacks):
        self.server_ip = server_ip
        self.client_ip = client_ip

    def start(self):
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clientsocket.connect((self.server_ip, 8087))

        self.read_from_server()


class ChatClient(ClientConnection):

    """Takes care of initializing the client for chat."""

    def __init__(self, server_ip, client_ip, callbacks):
        ClientConnection.__init__(self, server_ip, client_ip, callbacks)
        self.ready_for_chat, self.on_send, self.on_receive = callbacks

    def read_from_server(self):
        self.thread = Thread(target=self.printer)
        self.thread.daemon = True
        self.thread.start()

        self.ready_for_chat(self.send_message)

    def send_message(self, message):
        self.clientsocket.send(message.encode())
        self.on_send(message)

    def printer(self):
        while True:
            buf = self.clientsocket.recv(128)
            if len(buf) > 0:
                user = getpass.getuser()
                message = buf.decode()
                self.on_receive(user, self.client_ip, message)


class TransferClient(ClientConnection):

    """Takes care of initializing the server endpoint for transfer."""

    def __init__(self, server_ip, client_ip, callbacks):
        ClientConnection.__init__(self, server_ip, client_ip, callbacks)
        self.transfer_send, self.transfer_receive = callbacks

    def read_from_server(self):
        while True:
            buf = self.clientsocket.recv(128)
            if len(buf) > 0:
                self.transfer_receive(buf)
            else:
                break
        self.clientsocket.close()
