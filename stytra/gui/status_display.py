from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt5.QtGui import QPalette
from collections import OrderedDict
from datetime import datetime
import colorspacious
from queue import Empty
import numpy as np


def _hex_to_rgb(hex):
    hex = hex.lstrip("#")
    return tuple(int(hex[i * 2 : i * 2 + 2], 16) for i in range(3))


color_dict = dict(I=(25, 35, 44), P=(25, 35, 44), E=(143, 0, 1), W=(19, 76, 80))


class DisplayedMessage(QLabel):
    """A label for status messages which can optionally fade out"""

    def __init__(self, message, persist=0):
        super().__init__(message[2:])
        self.type = message[0]
        self.started = datetime.now()
        if self.type == "P":
            self.persist = -1
        else:
            self.persist = persist
        self.start_color = np.array(color_dict[self.type])
        self.end_color = np.nan_to_num(
            _hex_to_rgb(self.palette().color(QPalette.Button).name())
        )

    def is_expired(self, t):
        if self.persist > 0 and (t - self.started).total_seconds() > self.persist:
            return True
        return False

    def refresh(self):
        self.started = datetime.now()

    def update_t(self, t):
        if self.persist <= 0:
            return
        passed = (t - self.started).total_seconds() / self.persist

        color_bg = (self.end_color * passed + (1 - passed) * self.start_color).astype(
            np.uint8
        )
        color_txt = int(255 * (1 - passed))
        self.setStyleSheet(
            "background_color: rgb({},{},{});"
            " color: rgb({},{},{});".format(*color_bg, *((color_txt,) * 3))
        )


class StatusMessageDisplay(QWidget):
    def __init__(self):
        super().__init__()
        self.setLayout(QHBoxLayout())
        self.queues = []
        self.current_messages = OrderedDict()
        self.new_messages = []

    def addMessageQueue(self, queue):
        self.queues.append(queue)

    def addMessage(self, message, persist=3):
        if len(message) < 2:
            return
        if message in self.current_messages.keys():
            self.current_messages[message].refresh()

        else:
            self.current_messages[message] = DisplayedMessage(message, persist=persist)
            self.new_messages.append(self.current_messages[message])

    def refresh(self):
        for queue in self.queues:
            while True:
                try:
                    msg = queue.get(timeout=0.001)
                    self.addMessage(msg)
                except Empty:
                    break

        t = datetime.now()
        for msg in self.new_messages:
            self.layout().addWidget(msg)

        for key in list(self.current_messages.keys()):
            if self.current_messages[key].is_expired(t):
                self.layout().removeWidget(self.current_messages[key])
                self.current_messages.pop(key)
            else:
                self.current_messages[key].update_t(t)
