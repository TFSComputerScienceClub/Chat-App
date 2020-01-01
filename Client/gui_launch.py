import sys

from PyQt5.QtWidgets import QApplication, QWidget, QTabWidget, QVBoxLayout

from GUI.Tabs.SettingsTab import Settings
from GUI.Tabs.TextChat import TextChat

app = QApplication(sys.argv)


class ChatAppMainWindow(QWidget):

    def __init__(self):
        super(QWidget, self).__init__()

        self.tabs = QTabWidget()
        self.SettingsTab = Settings(self.tabs)
        self.TextChatTab = TextChat(self.tabs)

        self.setupUI()

    def add_tabs(self):
        self.tabs.addTab(self.TextChatTab, 'TextChat')
        self.tabs.addTab(self.SettingsTab, 'Settings')

    def setupUI(self):
        self.setWindowTitle('TFS Chat App')
        self.root_layout = QVBoxLayout(self)
        self.root_layout.setObjectName('MainWindow_root_layout')
        self.add_tabs()
        self.root_layout.addWidget(self.tabs)

        with open('tfsc.css', 'r') as styles:
            self.setStyleSheet(styles.read())


page = ChatAppMainWindow()

page.show()
app.exec()
