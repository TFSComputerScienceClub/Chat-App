from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLayout
from GUI.CustomWidgets.SettingsTextField import SettingsField
from JSONSettings  import SettingsService


class Settings(QWidget):
    def __init__(self, parent=None):
        super(Settings, self).__init__(parent=parent)
        self.setting_fields = []
        self.parent = parent
        self.setupUI()
        self.load_settings()

    # Simple JSON Hard coded loading...
    def load_settings(self):
        settings = SettingsService.load_settings()

        # Adds dictionary  to fields based on there objectNames, VERY IMPORTANT TO HAVE  A CONSISTENT objectName
        if isinstance(settings, dict):
            for field in self.setting_fields:
                key = field.objectName()
                field.setText(settings.get(key))

    def get_all_settings_fields(self, layout):
        widget_count = layout.count()
        for index in range(0, widget_count):
            widget = layout.itemAt(index)
            if isinstance(widget, QLayout):
                # Recursive call
                self.get_all_settings_fields(widget)
            else:
                widget = widget.widget()
                if isinstance(widget, SettingsField):
                    self.setting_fields.append(widget)

    def save_settings(self):
        settings_dict = {}

        # Compile fields text to dictionary based on each field objectName
        for field in self.setting_fields:
            settings_dict[field.objectName()] = field.text()
        SettingsService.save(settings_dict)

    def set_signal_for_all_fields(self):
        for field in self.setting_fields:
            field.OutFocusSignal.connect(self.save_settings)

    def setupUI(self):
        self.root_vbox = QVBoxLayout(self)

        self.username_label = QLabel('User Name: ')
        self.username_field = SettingsField('UserName')

        self.username_field.setObjectName('UserName')

        self.username_hbox = QHBoxLayout()

        self.username_hbox.setAlignment(Qt.AlignTop)

        self.username_hbox.addWidget(self.username_label)
        self.username_hbox.addWidget(self.username_field)

        self.root_vbox.addLayout(self.username_hbox)

        self.get_all_settings_fields(self.layout())
        self.set_signal_for_all_fields()
