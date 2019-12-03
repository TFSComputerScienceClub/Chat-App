import socket
import threading
from DevTools.devtools import dev_mode

# Static  global variables in Python.

'''
Static variables won't be to important,
 but nonetheless is very useful to understand sooner the better.
 
 https://radek.io/2011/07/21/static-variables-and-methods-in-python/
'''

ip = '192.168.0.13'
port = 25567


# TODO: Add Error Handling for listen and sending functions for the event of a socket disconnection.

class ClientHandler(threading.Thread):
    """
        Client Handler will be used to delegate incoming connections to it's own object and have the objects separately
        listening to oncoming messages in a separate thread from the main.

        Client Handler expects an socket object, the socket's address, and a optional receive function which
        requires an function that passes a parameter of bytes.

        Programming Concepts:
            OOP (Object-Oriented-Programming) -> https://realpython.com/python3-object-oriented-programming/
            Threading -> https://realpython.com/intro-to-python-threading/

    """

    def __init__(self, client_sock, address, on_receive=None):
        self.client_sock = client_sock
        self.address = address
        self.on_receive = on_receive

        if (self.on_receive is None) and dev_mode:
            print("WARNING NO FUNCTION LISTENING FOR CLIENT SOCK ", address)

        super(self.__class__, self).__init__(target=self.listen)

    def send(self, msg):
        self.client_sock.send(msg)

    def listen(self):

        while True:
            # Wait for message
            msg = self.client_sock.recv(1000)
            if not msg:
                print('client disconnected')
                break

            # If function is  callable  will send to custom function
            if callable(self.on_receive):
                print('Sending "{}" from {}  server.py  LINE 28'.format(msg, self.address))
                self.on_receive(msg)


class Server:
    """
    Server wait for new clients to connect and hands the sockets to a ClientHandler and adds the ClientHandler to
    the clients list and when new messages come from a ClientHandler, the message gets broad-casted to all currently
     connected clients.
    """

    def __init__(self):
        self.clients = []
        self.server_sock = socket.socket()
        self.server_sock.bind((ip, port))
        self.server_sock.listen(1)

    def broadcast_message(self, msg):
        for client in self.clients:
            client.send(msg)  # encode message to string

    def start(self):
        t1 = threading.Thread(target=self.handle_new_clients)
        t1.start()

    def handle_new_clients(self):
        while True:
            client_sock, address = self.server_sock.accept()

            new_client = ClientHandler(client_sock, address, self.broadcast_message)
            new_client.start()

            # test Message for new user connecting
            msg = "Hello! your address is " + str(address) + "!"
            new_client.send(msg.encode())

            self.clients.append(new_client)  # add new client_handler to clients list for later use.
            print('clients length now  = ', len(self.clients))


if __name__ == '__main__':
    server = Server()
    server.start()
