#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import calendar
import os
from datetime import datetime, timedelta

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow
from dateutil import rrule

from ui.CalcFuntions import CalcFunctionUtils
from ui.Constants import Constants
from ui.GuiForm import Ui_GuiForm


class GuiWinAdap(QMainWindow, Ui_GuiForm):
    """
    计算利息和详情信号，所有执行操作公用一个信号槽
    @本金
    @利率
    @利率单位
    @分期数目
    @分期类型
    @起始时间
    @结束时间
    """
    optCalcForExecutionSignal = pyqtSignal([float, float, str, int, str, str, str, str])

    """
    启用按照起止日志计算的信号
    @或者   提供分期或者起止时间（首次存款和末次存款时间）
    """
    optStageCheckBoxSignal = pyqtSignal([bool])

    # 起止时间计算利息和详情信号
    optCalcCapitalByStartEndDateSignal = pyqtSignal([float, float, str, str, str, str, str])

    def __init__(self, parent=None):
        super(GuiWinAdap, self).__init__(parent)
        self.setupUi(self)
        self.initUI()

    def initUI(self):
        # 按照分期触发计算
        self.optCalcCapital.clicked.connect(self.emitOptCalcCapitalSignal)
        self.optCalcForExecutionSignal[float, float, str, int, str, str, str, str].connect(
            self.calcCapitalInterestTotalAction)

        # 按照日期计算功能触发
        self.stageCheckBox.clicked.connect(self.emitOptCalcByDateSignal)
        self.optStageCheckBoxSignal[bool].connect(self.calcByDateAction)

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
            self.stageCheckBox_2.setDisabled(False)
        else:
            self.period.setDisabled(False)
            self.startDateEdit.setDisabled(True)
            self.endDateEdit.setDisabled(True)
            self.stageCheckBox_2.setDisabled(True)

    def emitOptCalcCapitalSignal(self, ):
        """发起计算利息信号"""
        print("begin emit calc signal...")
        self.optCalcForExecutionSignal[float, float, str, int, str, str, str, str].emit(
            self.capitalMoney.value(),
            self.interestRate.value(),
            self.interestRateDim.currentText(),
            self.period.value(),
            self.periodDim.currentText(),
            self.calcType.currentText(),
            self.startDateEdit.date().toString(Constants.DATE_TEMPLATE),
            self.endDateEdit.date().toString(Constants.DATE_TEMPLATE))

    def calcCapitalInterestTotalAction(self, capital, interestRate, interestRateDim, period, periodDim, calcType,
                                       startDate: str, endDate: str):
        """
        具体计算的动作
        :param capital: 本金
        :param interestRate: 利息
        :param interestRateDim: 利息单位
        :param period: 分期数目
        :param periodDim: 分期类型
        :param calcType: 计算类型
        :param startDate: 首次存款时间
        :param endDate: 末次存款时间
        :return:
        """
        print("receive calc signal...")

        if not self.stageCheckBox.isChecked():
            [ct, it, cit] = CalcFunctionUtils.calcResult(capital, interestRate,
                                                         interestRateDim, period,
                                                         periodDim, calcType)

            messages = CalcFunctionUtils.printDetails(capital, interestRate,
                                                      interestRateDim, period,
                                                      periodDim, calcType)
            self.capitalTotal.setText("%0.2f" % ct)
            self.interestTotal.setText("%0.2f" % it)
            self.capitalInterestTotal.setText("%0.2f" % cit)
            self.detailsText.setPlainText("{}".format(os.linesep.join(messages)))
            return

        # period 无效，需要重新计算
        startDateT = datetime.strptime(startDate, Constants.DATE_TEMPLATE_PY)
        endDateT = datetime.strptime(endDate, Constants.DATE_TEMPLATE_PY)
        if endDateT < startDateT:
            # TODO 弹出对话框，
            return

        [_, _, _, period] = GuiWinAdap.getPeriodByDate(endDateT, startDateT,
                                                       periodDim)
        [ct, it, cit] = CalcFunctionUtils.calcResult(capital, interestRate,
                                                     interestRateDim, period - 1,
                                                     periodDim, calcType)
        messages = CalcFunctionUtils.printDetails(capital, interestRate,
                                                  interestRateDim, period - 1,
                                                  periodDim, calcType)
        ct += capital
        cit += capital
        lastIt = 0
        if self.stageCheckBox_2.isChecked():
            # 可根据起始日期生成结束日期，后面补充确定
            daysLeft = (datetime.now() - endDateT).days
            [ct2, it2, cit2] = CalcFunctionUtils.calcResult(
                cit, interestRate,
                interestRateDim, daysLeft,
                Constants.PERIOD_BY_DAY,
                Constants.CALC_BY_SINGLE_RATE if calcType == Constants.CALC_BY_SINGLE_RATE else Constants.CALC_BY_COMPOUND_RATE)
            lastIt = it2

        # 最后一期的打印时间显示
        if calcType == Constants.CALC_BY_PERIOD_SINGLE_RATE or calcType == Constants.CALC_BY_PERIOD_COMPOUND_RATE:
            messages.append(Constants.TEMPLATE2.format(period, ct, lastIt, cit))

        it += lastIt
        cit += lastIt

        # 处理打印信息
        infos = list()
        infos.append(messages.pop(0))
        timeInfo = startDateT
        for msg in messages:
            curMonthDays = GuiWinAdap.getCurDateMaxMonthDays(timeInfo)
            if timeInfo.day < startDateT.day:
                timeInfo = timeInfo.replace(day=curMonthDays)
            infos.append("{}{}{}".format(timeInfo.strftime(Constants.DATE_TEMPLATE_PY), Constants.TEMPLATE_SEQ, msg))
            timeInfo = GuiWinAdap.getNextDate(timeInfo, periodDim)

        self.capitalTotal.setText("%0.2f" % ct)
        self.interestTotal.setText("%0.2f" % it)
        self.capitalInterestTotal.setText("%0.2f" % cit)
        self.detailsText.setPlainText("{}".format(os.linesep.join(infos)))
        return

    @staticmethod
    def getCurDateMaxMonthDays(dt: datetime):
        curYear = dt.year
        curMonth = dt.month
        nextYear = curYear
        nextMonth = curMonth + 1
        if nextMonth > Constants.RATE_YEAR_MONTH:
            nextYear += 1
            nextMonth = 1
        startT = dt.replace(day=1)
        endT = dt.replace(year=nextYear, month=nextMonth, day=1)
        return (endT - startT).days

    @staticmethod
    def getNextDate(startDate, periodDim):
        if periodDim == Constants.PERIOD_BY_YEAR:
            startDate = startDate.replace(year=(startDate.year + 1))
        elif periodDim == Constants.PERIOD_BY_MONTH:
            tmpYear = startDate.year
            tmpMonth = startDate.month + 1
            tmpDay = startDate.day
            if tmpMonth > Constants.RATE_YEAR_MONTH:
                tmpYear += 1
                tmpMonth = 1
            maxDaysOfMonth = GuiWinAdap.getCurDateMaxMonthDays(startDate.replace(year=tmpYear, month=tmpMonth, day=1))
            tmpDay = tmpDay if startDate.day <= maxDaysOfMonth else maxDaysOfMonth
            startDate = startDate.replace(year=tmpYear, month=tmpMonth, day=tmpDay)
        elif periodDim == Constants.PERIOD_BY_DAY:
            startDate += timedelta(days=1)
        else:
            pass
        return startDate

    @staticmethod
    def getPeriodByDate(endDateT, startDateT, periodDim):
        timeDelta = endDateT - startDateT
        periodByYears = rrule.rrule(rrule.YEARLY, dtstart=startDateT, until=endDateT).count()
        periodByMonths = rrule.rrule(rrule.MONTHLY, dtstart=startDateT, until=endDateT).count()
        periodByDays = timeDelta.days

        period = periodByDays
        if periodDim == Constants.PERIOD_BY_YEAR:
            period = periodByYears
        elif periodDim == Constants.PERIOD_BY_MONTH:
            period = periodByMonths

        return [periodByYears, periodByMonths, periodByDays, period]
