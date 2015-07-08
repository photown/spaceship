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

    if len(args) > 1 and args[1] == 'chat':
        init_chat(args)
    else:
        init_transfer(args)
    
def init_chat(args):
    channel = args[3] if len(args) > 3 and args[2] == '--channel' else ''

    current_ip = netifaces.ifaddresses("eth0")[AF_INET][0]['addr']
    current_handshake = BroadcastListener.BroadcastListener(current_ip, channel)
    current_handshake.start()

    is_server = current_handshake.is_server

    if is_server:
        server_ip = current_ip
        server_handshake = ServerBroadcast.ServerBroadcast(server_ip, channel, 'chat')
        server_handshake.start()
    else:
        client_connection = ClientConnection.ClientConnection(current_handshake.server_ip, current_ip, 'chat')
        client_connection.start()

def init_transfer(args):

    channel = args[2] if len(args) > 2 and args[1] == '--channel' else ''

    current_ip = netifaces.ifaddresses("eth0")[AF_INET][0]['addr']
    current_handshake = BroadcastListener.BroadcastListener(current_ip, channel)
    current_handshake.start()
    
    is_server = current_handshake.is_server

    if is_server:
        server_ip = current_ip
        server_handshake = ServerBroadcast.ServerBroadcast(server_ip, channel, 'transfer')
        server_handshake.start()
    else:
        client_connection = ClientConnection.ClientConnection(current_handshake.server_ip, current_ip, 'transfer')
        client_connection.start()

if __name__ == "__main__":
    main(sys.argv)