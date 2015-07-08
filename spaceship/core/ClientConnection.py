import socket
import sys
from threading import Thread
import getpass

class ClientConnection:
    def __init__(self, server_ip, client_ip, mode):
        self.server_ip = server_ip
        self.client_ip = client_ip
        self.mode = mode

    def start(self):
        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientsocket.connect((self.server_ip, 8087))

        self.read_from_server()

    def read_from_server(self):
        if self.mode == 'transfer':
            while True:
                buf = self.clientsocket.recv(128)
                if len(buf) > 0:
                    sys.stdout.buffer.write(buf)
                else:
                    break
            self.clientsocket.close()
        elif self.mode == 'chat':
            self.thread = Thread(target = self.printer)
            self.thread.daemon = True
            self.thread.start()

            while True:
                try:
                    data = input("")
                    self.clientsocket.send(data.encode())
                    print('\r\033[1A\033[0;;35mme: ' + data + '\033[0m')
                except KeyboardInterrupt:
                    self.clientsocket.close()
                    break
            
            
    def printer(self):
        while True:
            buf = self.clientsocket.recv(128)
            if len(buf) > 0:
                    print('\033[0;;34m' + getpass.getuser() + "<" + self.client_ip + ">: " + buf.decode() + '\033[0m')
            #else:
            #    break