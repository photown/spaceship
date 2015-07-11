import unittest
import socket
from threading import Thread
import threading
from time import time
from core.ClientConnection import ClientConnection
from core.ServerConnection import ServerConnection
from core.ServerBroadcast import ServerBroadcast
from core.BroadcastListener import BroadcastListener

class BufferSimulator:

    def __init__(self):
        self.counter = 5

    def read(self, bytes):
        self.counter -= 1
        if self.counter == 0:
            return 0
        return "puppies".encode()


class TestSockets(unittest.TestCase):

    def test_tcp_chat(self):
        callbacks = (self.ready_for_chat, self.on_send, self.on_receive)
        args = (callbacks, )
        self.thread = Thread(target = self.init_tcp_chat_server, args=args)
        self.thread.daemon = True
        self.thread.start()

        self.timer = threading.Timer(1, self.init_tcp_chat_client)
        self.timer.start()

        self.tcp_chat_response = None

    def init_tcp_chat_client(self):
        callbacks = (self.ready_for_chat, self.on_send, self.on_receive)
        client_connection = ClientConnection('localhost', 'localhost', 'chat', callbacks)
        client_connection.start()

        self.timer = threading.Timer(0.5, self.check_if_response)
        self.timer.start()

    def check_if_response(self):
        self.assertEquals(self.tcp_chat_response, 'puppies')
 
    def init_tcp_chat_server(self, callbacks):
        server_connection = ServerConnection('localhost', 'chat', callbacks)
        server_connection.start()

    def ready_for_chat(self, send_message):
        send_message("puppies")

    def on_receive(self, user, ip, message):
        self.tcp_chat_response = message

    def on_send(self, message):
        pass

    def test_tcp_transfer(self):
        callbacks = (self.transfer_tcp_send, self.transfer_tcp_receive)
        args = (callbacks, )
        self.thread = Thread(target = self.init_tcp_transport_server, args=args)
        self.thread.daemon = True
        self.thread.start()

        self.timer = threading.Timer(1, self.init_tcp_transport_client)
        self.timer.start()

    def transfer_tcp_send(self, stream_buffer):
        stream_buffer(BufferSimulator())

    def transfer_tcp_receive(self, buf):
        self.assertEquals(buf.decode(), 'puppies' * 4)

    def init_tcp_transport_client(self):
        callbacks = (self.transfer_tcp_send, self.transfer_tcp_receive)
        client_connection = ClientConnection('localhost', 'localhost', 'transfer', callbacks)
        client_connection.start()

    def init_tcp_transport_server(self, callbacks):
        server_connection = ServerConnection('localhost', 'transfer', callbacks)
        server_connection.start()

    def test_udp_pair_same_channels(self):
        self.udp_pair_helper("puppies", "puppies")

    def test_udp_pair_different_channels(self):
        self.udp_pair_helper("puppies", "kittens", True)
        
    def udp_pair_helper(self, broadcast_channel, listener_channel, are_different=False):
        callbacks = (self.transfer_send, self.transfer_receive)

        args = (callbacks, listener_channel)
        self.thread = Thread(target = self.init_udp_server, args=args)
        self.thread.daemon = True
        self.thread.start()

        self.start_time = time()

        listener = BroadcastListener('localhost', broadcast_channel)
        listener.start()

        response_time = time() - self.start_time

        if are_different:
            self.assertTrue(response_time > 0.9)
        else:
            self.assertTrue(response_time < 0.9)

    def init_udp_server(self, callbacks, channel):
        server_broadcast = ServerBroadcast("", channel, 'transfer', callbacks)
        server_broadcast.setup_socket()

    def transfer_send(self, stream_buffer):
        pass

    def transfer_receive(self, stream_buffer):
        pass

if __name__ == '__main__':
    unittest.main()