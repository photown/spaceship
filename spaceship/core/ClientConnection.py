import socket
import sys
from threading import Thread
import getpass

class ClientConnection:
    def __init__(self, server_ip, client_ip, mode, callbacks):
        self.server_ip = server_ip
        self.client_ip = client_ip
        self.mode = mode

        if mode == 'chat':
            self.ready_for_chat, self.on_send, self.on_receive = callbacks
        elif mode == 'transfer':
            self.transfer_send, self.transfer_receive = callbacks

    def start(self):
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientsocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clientsocket.connect((self.server_ip, 8087))

        self.read_from_server()

    def read_from_server(self):
        if self.mode == 'transfer':
            while True:
                buf = self.clientsocket.recv(128)
                if len(buf) > 0:
                    self.transfer_receive(buf)
                else:
                    break
            self.clientsocket.close()
        elif self.mode == 'chat':
            self.thread = Thread(target = self.printer)
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
                self.on_receive(getpass.getuser(), self.client_ip, buf.decode())