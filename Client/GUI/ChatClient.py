from Sockets.client import SocketClient
from PyQt5.Qt import QObject, pyqtSignal


class ChatClient(SocketClient, QObject):
    OnReceive = pyqtSignal(str)


    def emit_receive(self, msg):
        self.OnReceive.emit(msg.decode('utf-8'))

    def __init__(self, ip, port):
        super(ChatClient, self).__init__(ip, port)
        super(QObject, self).__init__()
        self.on_receive = self.emit_receive
