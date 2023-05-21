#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import os
import sys

from PyQt5.QtWidgets import QApplication

from gui.GuiWinAdap import GuiWinAdap

if __name__ == '__main__':
    sys.path.append(os.path.dirname(sys.path[0]))
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)

    win = GuiWinAdap()
    win.show()
    sys.exit(app.exec_())
