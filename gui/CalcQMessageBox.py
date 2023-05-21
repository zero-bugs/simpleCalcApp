#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from PyQt5.QtWidgets import QMessageBox


class CalcQMessageBox(QMessageBox):
    def __init__(self, parent=None):
        super(CalcQMessageBox, self).__init__(parent)
        self.setWindowTitle('计算工具提示信息')
        self.resize(100, 100)
        self.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        self.setDefaultButton(QMessageBox.Ok)
