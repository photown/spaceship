import socket
import sys
from threading import Thread
import getpass
import os

class ServerConnection:
    def __init__(self, server_ip, mode):
        self.server_ip = server_ip
        self.is_connected = False
        self.mode = mode

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
            sys.stdin = sys.stdin.detach();
            while True:
                data = sys.stdin.read(128)
                connection.send(data)
                if not data:
                    connection.close()
                    self.serversocket.close()
                    break
        elif self.mode == 'chat':
            self.thread = Thread(target = self.printer)
            self.thread.daemon = True
            self.thread.start()

            while True:
                try:
                    data = input("")
                    connection.send(data.encode())
                    print('\r\033[1A\033[0;;35mme: ' + data + '\033[0m')
                except KeyboardInterrupt:
                    connection.close()
                    self.serversocket.close()
                    break

    def printer(self):
        while True:
            buf = self.connection.recv(128)
            if len(buf) > 0:
                    print('\033[0;;34m' + getpass.getuser() + "<" + self.server_ip + ">: " + buf.decode() + '\033[0m')

