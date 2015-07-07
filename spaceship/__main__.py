import sys
import socket
import io
import time, threading, traceback
import fcntl
import struct
import netifaces
from netifaces import AF_INET
from core import ServerHandshake, ClientHandshake

def main(args=None):
    global server_handshake
    global client_handshake

    is_server = False
    
    if len(args) > 1 and args[1] == 'server':
        is_server = True
    
    if is_server:
        server_ip = netifaces.ifaddresses("eth0")[AF_INET][0]['addr']
        server_handshake = ServerHandshake.ServerHandshake(server_ip)
        server_handshake.start()
    else:
        client_ip = netifaces.ifaddresses("eth0")[AF_INET][0]['addr']
        client_handshake = ClientHandshake.ClientHandshake(client_ip)
        client_handshake.start()
    

if __name__ == "__main__":
    main(sys.argv)