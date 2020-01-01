from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLineEdit


# Overridden QLineEdit so we can react when a user clicks off of a  SettingsField
class SettingsField(QLineEdit):
    OutFocusSignal = pyqtSignal()

    def __init__(self, object_name):
        super(SettingsField, self).__init__()
        self.setObjectName(object_name)
        self.focus_out = None

    # Runs Every time a user clicks off of this field.
    def focusOutEvent(self, QFocusEvent):

        super(SettingsField, self).focusOutEvent(QFocusEvent)

        self.OutFocusSignal.emit()
