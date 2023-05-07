#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import os

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow

from ui.CalcFuntions import CalcFunctionUtils
from ui.GuiForm import Ui_GuiForm


class GuiWinAdap(QMainWindow, Ui_GuiForm):
    capitalSignal = pyqtSignal(float)
    interestRateSignal = pyqtSignal(float)
    periodSignal = pyqtSignal(int)

    # 函数信号
    optCalcCapitalSignal = pyqtSignal([float, float, str, int, str, str])
    optCalcDetailsSignal = pyqtSignal([float, float, str, int, str, str])

    def __init__(self, parent=None):
        super(GuiWinAdap, self).__init__(parent)
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        self.optCalcCapital.clicked.connect(self.emitOptCalcCapitalSignal)
        self.optCalcCapitalSignal[float, float, str, int, str, str].connect(self.calcCapitalInterestTotal)

        self.optCalcDetails.clicked.connect(self.emitOptCalcDetails)
        self.optCalcDetailsSignal[float, float, str, int, str, str].connect(self.calcCapitalInterestDetails)

    def emitOptCalcCapitalSignal(self, ):
        """发起计算利息信号"""
        # print("begin emit calc signal...")
        self.optCalcCapitalSignal[float, float, str, int, str, str].emit(self.capitalMoney.value(),
                                                                         self.interestRate.value(),
                                                                         self.interestRateDim.currentText(),
                                                                         self.period.value(),
                                                                         self.periodDim.currentText(),
                                                                         self.calcType.currentText())

    def calcCapitalInterestTotal(self, capital, interestRate, interestRateDim, period, periodDim, calcType):
        # print("receive calc signal...")
        [ct, it, cit] = CalcFunctionUtils.calcResult(capital, interestRate,
                                                     interestRateDim, period,
                                                     periodDim, calcType)
        self.capitalTotal.setText("%0.2f" % ct)
        self.interestTotal.setText("%0.2f" % it)
        self.capitalInterestTotal.setText("%0.2f" % cit)

    def emitOptCalcDetails(self):
        """发起计算利息信号"""
        # print("begin emit details signal...")
        self.optCalcDetailsSignal[float, float, str, int, str, str].emit(self.capitalMoney.value(),
                                                                         self.interestRate.value(),
                                                                         self.interestRateDim.currentText(),
                                                                         self.period.value(),
                                                                         self.periodDim.currentText(),
                                                                         self.calcType.currentText())

    def calcCapitalInterestDetails(self, capital, interestRate, interestRateDim, period, periodDim, calcType):
        # print("receive details signal...")
        messages = CalcFunctionUtils.printDetails(capital, interestRate,
                                                  interestRateDim, period,
                                                  periodDim, calcType)
        self.detailsText.setPlainText("{}".format(os.linesep.join(messages)))
