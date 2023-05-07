#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import os
import sys

from PyQt5.QtWidgets import QApplication

from ui.GuiWinAdap import GuiWinAdap

sys.path.append(os.path.dirname(sys.path[0]))
app = QApplication(sys.argv)
win = GuiWinAdap()
win.show()
sys.exit(app.exec_())
