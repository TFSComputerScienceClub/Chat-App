# Python json library https://www.w3schools.com/python/python_json.asp
import json
import os

SETTINGS_FILENAME = 'settings.TFSC'

settings = {}


def load_settings():
    global settings
    settings_ = None
    if not os.path.exists(SETTINGS_FILENAME):
        with open(SETTINGS_FILENAME, 'w'): pass

    with open('settings.TFSC', 'r') as settings_file:
        try:

            settings_ = json.load(settings_file)
        except Exception as e:
            pass
    settings = settings_
    return settings_


def save(settings_dict):
    global settings
    with open(SETTINGS_FILENAME, 'w') as settings_file:
        json.dump(settings_dict, settings_file)
    settings = settings_dict
