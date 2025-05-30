from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

# 可按下的按钮，实现状态切换时开关车流模拟
class ToggleButton(QPushButton):

    change_to_on = pyqtSignal()
    change_to_off = pyqtSignal()

    def __init__(self, name):
        super().__init__()

        self.state = 'off'

        self.setText(name)
        self.setCheckable(True)

        self.clicked.connect(self.change_state)

    def change_state(self):
        if self.state == 'off':
            self.state = 'on'

            self.change_to_on.emit()

        elif self.state == 'on':
            self.state = 'off'

            self.change_to_off.emit()