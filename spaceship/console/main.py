import sys
import socket
import io
import time
import threading
import traceback
import fcntl
import struct
import netifaces
from netifaces import AF_INET
from core.Handshake import Handshake, ServerBroadcast, BroadcastListener


class Main:
    def __init__(self, args):

        """Entry point for the whole project."""

        ip = netifaces.ifaddresses("eth0")[AF_INET][0]['addr']
        num = len(args)

        if len(args) > 1 and args[1] == 'chat':
            channel = args[3] if num > 3 and args[2] == '--channel' else ''
            mode = 'chat'
            callbacks = (self.ready_for_chat, self.on_send, self.on_receive)

        else:

            channel = args[2] if num > 2 and args[1] == '--channel' else ''
            mode = 'transfer'
            callbacks = (self.transfer_send, self.transfer_receive)

        try:
            Handshake(ip, channel, mode, callbacks).start()
        except KeyboardInterrupt:
            pass

    def ready_for_chat(self, send_message):
        print("connected")
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
