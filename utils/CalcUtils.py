#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from datetime import datetime, timedelta

from utils.Constants import Constants


class CalcUtils:
    @staticmethod
    def guessPeriodByDate(startDateT, endDateT, periodDim):
        """
        如果periodLeftDays>0，那么可能少计算几天，如果periodLeftDays<0，那么可能多计算几天，简单起见，不考虑这些场景
        按照起始日期推算分期数目的算法只考虑每月定存，月中某一天或者月末的一天，不考虑极端场景
        当然最精确的计算方式是每笔存款单独计息，但这样问题也变得复杂
        :param startDateT: 起始日期
        :param endDateT: 结束日期
        :param periodDim: 分期类型
        :return:
        """
        timeDelta = endDateT - startDateT
        periodByDays = timeDelta.days
        if periodDim == Constants.PERIOD_BY_YEAR:
            period = round(periodByDays / Constants.RATE_YEAR_DAYS)
            periodByDays = periodByDays - period * Constants.RATE_YEAR_DAYS
        elif periodDim == Constants.PERIOD_BY_MONTH:
            period = round(periodByDays / Constants.RATE_MONTH_DAY)
            periodByDays = periodByDays - period * Constants.RATE_MONTH_DAY
        elif periodDim == Constants.PERIOD_BY_DAY:
            period = periodByDays
            periodByDays = 0
        else:
            print('unexpected error: wrong calc type.')
            period = 0
            periodByDays = 0

        return [periodByDays, period]

    @staticmethod
    def getCurMonthDays(dt: datetime):
        """获取本月有多少天"""
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
    def incrementYearAndGet(startDate: datetime, years):
        return startDate.replace(year=(startDate.year + years))

    @staticmethod
    def incrementMonthAndGet(startDate: datetime, months):
        tmpMonth = startDate.month + months

        tmpYear = startDate.year + int((tmpMonth - 1) / Constants.RATE_YEAR_MONTH)
        tmpMonth = ((tmpMonth - 1) % Constants.RATE_YEAR_MONTH + 1)
        monthDays = CalcUtils.getCurMonthDays(startDate.replace(year=tmpYear, month=tmpMonth, day=1))
        tmpDay = startDate.day if startDate.day < monthDays else monthDays
        return startDate.replace(year=tmpYear, month=tmpMonth, day=tmpDay)

    @staticmethod
    def incrementDayAndGet(startDate: datetime, days):
        return startDate + timedelta(days=days)

    @staticmethod
    def getNextDate(startDateT, curPeriod, periodDim):
        if periodDim == Constants.PERIOD_BY_YEAR:
            return CalcUtils.incrementYearAndGet(startDateT, curPeriod)
        elif periodDim == Constants.PERIOD_BY_MONTH:
            return CalcUtils.incrementMonthAndGet(startDateT, curPeriod)
        elif periodDim == Constants.PERIOD_BY_DAY:
            return CalcUtils.incrementDayAndGet(startDateT, curPeriod)
        else:
            pass

    @staticmethod
    def printMsgForTmpt3(lastIt, ct, cit, endDateT, period):
        return "{}{}{}".format(endDateT.strftime(Constants.DATE_TEMPLATE_PY), Constants.TEMPLATE_SEQ,
                               Constants.TEMPLATE2.format(period + 1, ct, lastIt, cit))

    @staticmethod
    def printMsgForTmpt2(ct, lastIt, cit, endDateT):
        return "{}{}{}".format(endDateT.strftime(Constants.DATE_TEMPLATE_PY), Constants.TEMPLATE_SEQ,
                               Constants.TEMPLATE3.format(ct, lastIt, cit))
