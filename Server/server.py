import socket
import threading
from DevTools.devtools import dev_mode

# Static  global variables in Python.

'''
Static variables won't be that important,
but nonetheless is very useful to understand sooner the better.
 
 https://radek.io/2011/07/21/static-variables-and-methods-in-python/
'''

ip_ = '192.168.0.13'
port_ = 25567


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

    def __init__(self, client_sock, address, on_receive=None, on_disconnected=None):
        self.client_sock = client_sock
        self.address = address
        self.stop = False
        self.on_receive = on_receive # function, params: data,client_handler
        # on_receive passes the received data and the client_handler its from.

        self.on_disconnected = on_disconnected

        if (self.on_receive is None) and dev_mode:
            print("WARNING NO FUNCTION LISTENING FOR CLIENT SOCK ", address)

        super(self.__class__, self).__init__(target=self.listen)

    def send(self, msg):
        try:
            self.client_sock.send(msg)
        except Exception:
            self.stop = True
            pass

    def listen(self):

        while True or not self.stop:
            try:

                # Wait for message
                msg = self.client_sock.recv(1000)
                if not msg:
                    print('client disconnected')
                    break

                # If function is  callable  will send to custom function
                if callable(self.on_receive):
                    print('Sending "{}" from {}  server.py  ClientHandler'.format(msg, self.address))
                    self.on_receive(msg, self)
            except Exception:
                pass
                break
        if callable(self.on_disconnected):
            self.on_disconnected(self)


class Server:
    """
    Server wait for new clients to connect and hands the sockets to a ClientHandler and adds the ClientHandler to
    the clients list and when new messages come from a ClientHandler, the message gets broad-casted to all currently
     connected clients.

     Server Object also expects a ClientHandlerDelegate, which is a function that will handle the process of creating a ClientHandler,
     the function must be in the form

     'delegate(client_socket, address_tuple):...return ClientHandler()'
    """

    def __init__(self, ip, port):

        self.clients = []
        self.client_obj = ClientHandler  # Made as variable  for user customization.
        self.server_sock = socket.socket()
        self.server_sock.bind((ip, port))
        self.server_sock.listen(1)

    def start(self):
        t1 = threading.Thread(target=self.handle_new_clients)
        t1.start()

    def remove_client(self, client):
        print('removing client...', client)
        self.clients.remove(client)

    def broadcast_message(self, msg, client_from):

        for client in self.clients:
            client.send(msg)  # encode message to string

    def handle_new_clients(self):

        while True:

            client_sock, address = self.server_sock.accept()
            try:
                invalid_client = False
                error_msg = None
                new_client = None
                if callable(self.client_obj):
                    new_client = self.client_obj(client_sock, address, on_receive=self.broadcast_message,
                                                 on_disconnected=self.remove_client)
                    if isinstance(new_client, ClientHandler):
                        new_client.start()
                    else:
                        invalid_client = True
                        error_msg = 'Invalid ClientHandler Delegator, self.client_handler_delegate() must return ClientHandler instead of {}'.format(
                            new_client)
                        break
                else:
                    invalid_client = True
                    error_msg = 'Invalid client_handler_delegator, must be callable'

                if invalid_client:
                    raise Exception(error_msg)

                # test Message for new user connecting
                # msg = "Hello! your address is " + str(address) + "!"
                # new_client.send(msg.encode())

                self.clients.append(new_client)  # add new client_handler to clients list for lat-er use.
                print('clients length now  = ', len(self.clients))
            except Exception as e:
                print(e)


# Temp Example
if __name__ == '__main__':
    server = Server(ip_, port_)
    server.start()
