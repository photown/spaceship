import sys
import socket
import io
import time, threading, traceback
import fcntl
import struct
import netifaces
from core import ClientConnection
from netifaces import AF_INET
from core import ServerBroadcast, BroadcastListener

def main(args=None):
    global server_handshake
    global client_handshake

    current_ip = netifaces.ifaddresses("eth0")[AF_INET][0]['addr']
    current_handshake = BroadcastListener.BroadcastListener(current_ip)
    current_handshake.start()

    keep_on(current_handshake, current_ip)

def keep_on(current_handshake, current_ip):
    global server_handshake
    global client_connection
    
    is_server = current_handshake.is_server

    if is_server:
        server_ip = current_ip
        server_handshake = ServerBroadcast.ServerBroadcast(server_ip)
        server_handshake.start()
    else:
        client_connection = ClientConnection.ClientConnection(current_handshake.server_ip, current_ip)
        client_connection.start()
    

if __name__ == "__main__":
    main(sys.argv)