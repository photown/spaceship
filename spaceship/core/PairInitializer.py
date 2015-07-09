from core.ServerBroadcast import ServerBroadcast
from core.BroadcastListener import BroadcastListener
from core.ClientConnection import ClientConnection

class PairInitializer:
    def __init__(self, ip, channel, mode, callbacks):
        self.ip = ip
        self.channel = channel
        self.mode = mode
        self.callbacks = callbacks

    def start(self):
        listener = BroadcastListener(self.ip, self.channel)
        listener.start()
        
        is_server = listener.is_server

        if is_server:
            broadcaster = ServerBroadcast(self.ip, self.channel, self.mode, self.callbacks)
            broadcaster.start()
        else:
            client_connection = ClientConnection(listener.server_ip, self.ip, self.mode, self.callbacks)
            client_connection.start()