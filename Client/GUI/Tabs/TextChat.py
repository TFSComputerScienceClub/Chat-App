from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QTextEdit

from GUI.ChatClient import ChatClient
from JSONSettings import SettingsService

from GUI.CustomWidgets.TextChatTextField import TextChatField

'''
Seperated 
'''


class TextChat(QWidget):
    def __init__(self, parent=None):
        super(TextChat, self).__init__(parent=parent)

        self.client_socket = ChatClient('192.168.0.22', 25565)
        self.client_socket.OnReceive.connect(self.add_text)
        self.setupUI()

    def add_text(self, text):
        self.text_area.append(text)

    def send_msg(self):
        text = self.send_field.text()
        self.send_field.clear()

        # Call ChatClient's backend code
        self.client_socket.send(text.encode('utf-8'))

    def connect(self):
        if self.client_socket.connected:
            self.text_area.append('\nYou are already connected!!')
        else:

            self.client_socket.start()
            self.client_socket.send(SettingsService.settings.get('UserName').encode('utf-8'))

    def setupUI(self):
        self.root_vbox = QVBoxLayout()

        self.root_vbox.setObjectName('MainWindow_root_vbox')
        self.connect_but = QPushButton('Connect To Server')

        self.connect_but.clicked.connect(self.connect)
        self.root_vbox.addWidget(self.connect_but)
        self.text_area = QTextEdit()

        self.root_vbox.addWidget(self.text_area)

        self.send_hbox = QHBoxLayout()

        self.send_button = QPushButton('Send')
        self.send_button.clicked.connect(self.send_msg)

        self.send_field = TextChatField(self.send_msg)

        self.send_hbox.addWidget(self.send_field)
        self.send_hbox.addWidget(self.send_button)

        self.root_vbox.addLayout(self.send_hbox)

        self.setLayout(self.root_vbox)
