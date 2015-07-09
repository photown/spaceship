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
from core.PairInitializer import PairInitializer

class Main:
    def __init__(self, args):

        ip = netifaces.ifaddresses("eth0")[AF_INET][0]['addr']

        if len(args) > 1 and args[1] == 'chat':
            channel = args[3] if len(args) > 3 and args[2] == '--channel' else ''
            mode = 'chat'
            callbacks = (self.ready_for_chat, self.on_send, self.on_receive)
            
        else:
            channel = args[2] if len(args) > 2 and args[1] == '--channel' else ''
            mode = 'transfer'
            callbacks = (self.transfer_send, self.transfer_receive)

        PairInitializer(ip, channel, mode, callbacks).start()

    def ready_for_chat(self, send_message):
        while True:
            try:
                data = input("")
                send_message(data)
            except KeyboardInterrupt:
                break

    def on_receive(self, user, ip, message):
        print('\033[0;;34m' + user + "<" + ip + ">: " + message + '\033[0m')

    def on_send(self, message):
        print('\r\033[1A\033[0;;35mme: ' + message + '\033[0m')

    def transfer_send(self, stream_buffer):
        sys.stdin = sys.stdin.detach()
        stream_buffer(sys.stdin)

    def transfer_receive(self, stream_buffer):
        sys.stdout.buffer.write(stream_buffer)



