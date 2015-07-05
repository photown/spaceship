import sys
import socket
import io
import time, threading, traceback

def init_server():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind(('192.168.1.100', 8089))
    serversocket.listen(5) # become a server socket, maximum 5 connections
    #print("listening")
    connection, address = serversocket.accept()

    while True:
        #print("READING WOHOO")       
        
        buf = connection.recv(128)
        if len(buf) > 0:
            sys.stdout.buffer.write(buf)
            #print(buf)
        else:
            break
    #print("done")

cs = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def init_server_handshake():
    
    #cs.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #cs.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    cs.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    #cs.bind(('', 8089))
    cs.bind(('192.168.1.100', 8089))
    handshake_server()

    while 1:
        try:
            print("waiting client affirmation")
            message, address = cs.recvfrom(128)
            print( "CLIENT AFFIRMED", address)
            #s.close()
            
            #s.close()
            #init_client(address[0])

        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            traceback.print_exc()

def handshake_server():
    
    cs.sendto('This is a test'.encode(), ('255.255.255.255', 8089))

    print("send")
    
    threading.Timer(1, handshake_server).start()

def handshake_client():
    host = '255.255.255.255'                               # Bind to all interfaces
    port = 8089

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.bind((host, port))

    while 1:
        try:
            print("waiting to receive")
            message, address = s.recvfrom(128)
            print( "Got data from", address)
            #s.close()
            
            # Acknowledge it.
            s.sendto("I am here".encode(), address)
            #s.close()
            #init_client(address[0])

        except (KeyboardInterrupt, SystemExit):
            raise
        except:
            traceback.print_exc()

def init_client(ip_address):
    clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientsocket.connect((ip_address, 8089))
    #filelike = io.StringIO(sys.stdin.buffer.read())
    #data = sys.stdin.readlines()
    '''while True:
        data = filelike.read(64)
        clientsocket.send(data.encode())
        if not data:
            break'''
    sys.stdin = sys.stdin.detach();
    while True:
        #print("WRITING WOHOO")
        data = sys.stdin.read(128)
        clientsocket.send(data)
        if not data:
            break
        
    clientsocket.close()

def main(args=None):
    is_server = False
    #print("args", args)
    
    if len(args) > 1 and args[1] == 'server':
        is_server = True
    
    if is_server:
        init_server_handshake()
        #init_server()
    else:
        handshake_client()
        #init_client()
    

if __name__ == "__main__":
    #print("printing args")
    #print(sys.argv)
    main(sys.argv)