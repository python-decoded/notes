"""
В даному прикладі ми очікуємо змінні оточення USER та PASSWORD
але вони можуть бути і не встановлені при локальному запуску тестів

та функцію get_connection всеодно треба якось протестувати
"""

import os

USER = os.environ['LOGIN']
PASSWORD = os.environ['PASSWORD']


def get_connection():
    if USER and PASSWORD:
        print("Connection is successful")
        return

    raise ConnectionError
