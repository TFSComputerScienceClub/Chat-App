from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLineEdit


'''
TextChatField is to a attach a function on a keypressevent waiting until the user presses enter on the field.
'''

class TextChatField(QLineEdit):
    def __init__(self, on_enter):
        self.on_enter = on_enter
        super(TextChatField, self).__init__()

    def keyPressEvent(self, QKeyEvent):
        super(TextChatField, self).keyPressEvent(QKeyEvent)

        if QKeyEvent.key() == Qt.Key_Enter-1:
            self.on_enter()
