import socket
import threading
from Commands import Commands
from Commands import CommandHandler
from Server.ClientHandler import ClientHandler
from DevTools.devtools import dev_mode

# Static  global variables in Python.

'''
Static variables won't be that important,
but nonetheless is very useful to understand sooner the better.
 
 https://radek.io/2011/07/21/static-variables-and-methods-in-python/
'''

ip_ = '192.168.0.22'
port_ = 25565


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
        Commands.set_server_reference(self)

    def start(self):
        t1 = threading.Thread(target=self.handle_new_clients)
        t1.start()

    # remove client from clients list,  and say who has left.
    def remove_client(self, client):
        print('removing client...', client)
        self.clients.remove(client)

        if len(self.clients) > 0:
            print('broadcasting')

            disconnect_msg = client.username + " Has disconnected!!"

            self.broadcast_message(disconnect_msg.encode('utf-8'), client)

    def broadcast_message(self, msg, client_from):
        is_command, output = CommandHandler.handle_message(msg.decode(), client_from)

        if is_command and isinstance(output, str):
            print('sending command?')
            client_from.send(output.encode('utf-8'))
        else:
            for client in self.clients:
                client.send(msg)  # encode message to string

    def handle_new_clients(self):

        while True:
            new_client = None
            client_sock, address = self.server_sock.accept()
            try:
                invalid_client = False

                if callable(self.client_obj):
                    new_client = self.client_obj(client_sock, address, on_receive=self.broadcast_message,
                                                 on_disconnected=self.remove_client)
                    self.clients.append(new_client)  # add new client_handler to clients list for later use.
                    if isinstance(new_client, ClientHandler):
                        new_client.start()



                else:
                    invalid_client = True
                    error_msg = 'Invalid client_handler_delegator, must be callable'



            except Exception as e:
                print(e)


# Temp Example
if __name__ == '__main__':
    server = Server(ip_, port_)

    server.start()
