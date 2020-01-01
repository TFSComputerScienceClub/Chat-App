import socket
import threading
from ErrorHandling.ErrorCheck import *

ip_ = '192.168.0.13'
port_ = 25567


class SocketClient:
    '''
    Read Server.py docstrings for further information
    '''

    def __init__(self, ip, port, on_receive=None):
        self.ip = ip
        self.connected = False
        self.port = port
        self.on_receive = None
        self.socket = None

        self.on_receive = on_receive

    def start(self):
        self.socket = socket.socket()

        try:
            self.socket.connect((self.ip, self.port))
        except Exception as e:
            print(e)
        t1 = threading.Thread(target=self.listen)
        t1.daemon = True
        t1.start()

    def listen(self):
        self.connected = True
        while True:
            msg = self.socket.recv(1000)
            if not msg:
                self.on_receive('Lost Connection.'.encode())
                self.connected = False
                break
            if callable(self.on_receive):
                self.on_receive(msg)

    def send(self, msg):
        try:
            if not self.connected:
                raise Exception('Not Connected!')
            self.socket.send(msg)
        except Exception as e:
            print(e)
            error = get_client_error(self.socket, e)

            self.on_receive('Error Sending message \"{}\"\nSocket Error: {}'.format(msg, error).encode())


if __name__ == '__main__':
    client = SocketClient(ip_, port_, lambda x: print('from server: ', x.decode()))
    client.start()
    while True:
        msg = input('Enter message to server:\n')
        print('sending "{}"'.format(msg))
        client.send(msg.encode())
