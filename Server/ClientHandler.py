import threading


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

    def __init__(self, client_sock, address, on_receive=None, on_disconnected=None, use_username=True):
        self.username = str

        self.admin = False
        self.use_username = use_username
        self.client_sock = client_sock
        self.address = address

        self.stop = False
        self.on_receive = on_receive  # function, params: data,client_handler
        # on_receive passes the received data and the client_handler its from.

        self.on_disconnected = on_disconnected

        if (self.on_receive is None) and dev_mode:
            print("WARNING NO FUNCTION LISTENING FOR CLIENT SOCK ", address)

        super(self.__class__, self).__init__(target=self.listen)

    def disconnect(self, reason=None):

        if isinstance(reason, str):
            self.send(reason.encode())

        self.client_sock.close()

    def send(self, msg: bytes):
        try:
            self.client_sock.send(msg)
        except Exception as e:
            self.stop = True
            pass

    def listen(self):

        if self.use_username:
            self.username = self.client_sock.recv(1000).decode()  # Expects first transmission to be username.
            self.on_receive('{} Has Connected!!'.format(self.username).encode('utf-8'), self)

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

                    self.on_receive((self.username + ": ").encode() + msg, self)
            except Exception as e:
                print(e)
                break
        if callable(self.on_disconnected):
            self.on_disconnected(self)
