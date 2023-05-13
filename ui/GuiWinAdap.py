#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import datetime
import os
from datetime import date

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow

from ui.CalcFuntions import CalcFunctionUtils
from ui.GuiForm import Ui_GuiForm


class GuiWinAdap(QMainWindow, Ui_GuiForm):
    # 分期计算利息和详情信号
    optCalcCapitalByPeriodSignal = pyqtSignal([float, float, str, int, str, str])

    # 起止时间计算利息和详情信号
    optCalcCapitalByStartEndDateSignal = pyqtSignal([float, float, str, str, str, str, str])

    # 启用按照起止日志计算的信号
    optStageCheckBoxSignal = pyqtSignal([bool])

    # 时间格式模板
    DATE_TEMPLATE = "yyyy/MM/dd"
    DATE_TEMPLATE_PY = "%Y/%m/%d"
    TIME_TEMPLATE = "%Y/%m/%d HH:mm:ss"

    def __init__(self, parent=None):
        super(GuiWinAdap, self).__init__(parent)
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        # 按照分期触发计算
        self.optCalcCapital.clicked.connect(self.emitOptCalcCapitalSignal)
        self.optCalcCapitalByPeriodSignal[float, float, str, int, str, str].connect(self.calcCapitalInterestTotalAction)
        self.optCalcCapitalByPeriodSignal[float, float, str, int, str, str].connect(
            self.calcCapitalInterestDetailsAction)

        # 按照起止日期触发计算
        self.optCalcCapital.clicked.connect(self.emitOptCalcCapitalByStartEndDateSignal)
        self.optCalcCapitalByStartEndDateSignal[float, float, str, str, str, str, str].connect(
            self.calcCapitalInterestTotalByDateAction)
        self.optCalcCapitalByStartEndDateSignal[float, float, str, str, str, str, str].connect(
            self.calcCapitalInterestDetailsByDateAction)

        # 按照日期计算功能触发
        self.stageCheckBox.clicked.connect(self.emitOptCalcByDateSignal)
        self.optStageCheckBoxSignal[bool].connect(self.calcByDateAction)

    def calcCapitalInterestTotalByDateAction(self, capital, interestRate, interestRateDim, startDate: str,
                                             endDate: str, periodDim, calcType):
        """按照起止日期计算利息"""
        startDateT = datetime.datetime.strptime(startDate, self.DATE_TEMPLATE_PY)
        endDateT = datetime.datetime.strptime(endDate, self.DATE_TEMPLATE_PY)
        if endDateT < startDateT:
            # TODO 弹出对话框，
            return

        timeDelta = endDateT - startDateT
        timeDeltaDays = timeDelta.days
        print(timeDeltaDays)

    def calcCapitalInterestDetailsByDateAction(self, capital, interestRate, interestRateDim, startDate, endDate,
                                               periodDim, calcType):
        """按照起止日期计算详细"""
        pass

    def emitOptCalcCapitalByStartEndDateSignal(self, ):
        """按照起止日志计算信息触发"""
        if not self.stageCheckBox.isChecked():
            return
        print("begin emit start calc by date signal...")
        self.optCalcCapitalByStartEndDateSignal[float, float, str, str, str, str, str].emit(
            self.capitalMoney.value(),
            self.interestRate.value(),
            self.interestRateDim.currentText(),
            self.startDateEdit.date().toString(self.DATE_TEMPLATE),
            self.endDateEdit.date().toString(self.DATE_TEMPLATE),
            self.periodDim.currentText(),
            self.calcType.currentText())

    def emitOptCalcByDateSignal(self, ):
        """选中启用起止日期功能"""
        print("begin emit start calc by date switch signal...")
        self.optStageCheckBoxSignal[bool].emit(self.stageCheckBox.isChecked())

    def calcByDateAction(self, isChecked):
        """启用起止日期功能按钮动作"""
        print("begin receive calc by date switch signal....")
        if isChecked:
            self.period.setDisabled(True)
            self.startDateEdit.setDisabled(False)
            self.endDateEdit.setDisabled(False)
        else:
            self.period.setDisabled(False)
            self.startDateEdit.setDisabled(True)
            self.endDateEdit.setDisabled(True)

    def emitOptCalcCapitalSignal(self, ):
        """发起计算利息信号"""
        if self.stageCheckBox.isChecked():
            return
        print("begin emit calc signal...")
        self.optCalcCapitalByPeriodSignal[float, float, str, int, str, str].emit(self.capitalMoney.value(),
                                                                                 self.interestRate.value(),
                                                                                 self.interestRateDim.currentText(),
                                                                                 self.period.value(),
                                                                                 self.periodDim.currentText(),
                                                                                 self.calcType.currentText())

    def calcCapitalInterestTotalAction(self, capital, interestRate, interestRateDim, period, periodDim, calcType):
        print("receive calc signal...")
        [ct, it, cit] = CalcFunctionUtils.calcResult(capital, interestRate,
                                                     interestRateDim, period,
                                                     periodDim, calcType)
        self.capitalTotal.setText("%0.2f" % ct)
        self.interestTotal.setText("%0.2f" % it)
        self.capitalInterestTotal.setText("%0.2f" % cit)

    def calcCapitalInterestDetailsAction(self, capital, interestRate, interestRateDim, period, periodDim, calcType):
        print("receive details signal...")
        messages = CalcFunctionUtils.printDetails(capital, interestRate,
                                                  interestRateDim, period,
                                                  periodDim, calcType)
        self.detailsText.setPlainText("{}".format(os.linesep.join(messages)))
