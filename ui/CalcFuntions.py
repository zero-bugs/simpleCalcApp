#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from urllib3.connectionpool import xrange

from ui.Constants import Constants


class CalcFunctionUtils:
    @staticmethod
    def calcFixCapitalSimpleInterest(capital, interestRate, period):
        """单利定存"""
        capitalMoney = capital
        interestMoney = capital * interestRate * period
        total = capitalMoney + interestMoney
        return [capitalMoney, interestMoney, total]

    @staticmethod
    def calcIncreCapitalSimpleInterest(capital, interestRate, period):
        """单利每月定存"""
        capitalMoney = period * capital
        interestMoney = capital * interestRate * period * (period + 1) / 2
        total = capitalMoney + interestMoney
        return [capitalMoney, interestMoney, total]

    @staticmethod
    def calcFixCapitalCompoundedInterest(capital, interestRate, period):
        """复利定存"""
        capitalMoney = capital
        interestMoney = capital * pow(1 + interestRate, period) - capital
        total = capitalMoney + interestMoney
        return [capitalMoney, interestMoney, total]

    @staticmethod
    def calcIncreCapitalCompoundedInterest(capital, interestRate, period):
        """复利每月定存"""
        capitalMoney = period * capital
        interestMoney = capital * ((1 + interestRate) / interestRate) * (
                pow(1 + interestRate, period) - 1) - capitalMoney
        total = capitalMoney + interestMoney
        return [capitalMoney, interestMoney, total]

    @staticmethod
    def calcAnnualToMonthInterest(capital, interestRate, period):
        return [0.0, 0.0, 0.0]

    @staticmethod
    def calcMonthToAnnualInterest(capital, interestRate, period):
        return [0.0, 0.0, 0.0]

    @staticmethod
    def rateConvert(interestRate, interestRateDim, periodDim):
        interestRate = interestRate / 100
        if periodDim == Constants.PERIOD_BY_YEAR:
            if interestRateDim == Constants.RATE_BY_MONTH:
                return 12 * interestRate
            elif interestRateDim == Constants.RATE_BY_DAY:
                return 365 * interestRate
            else:
                return interestRate
        elif periodDim == Constants.PERIOD_BY_MONTH:
            if interestRateDim == Constants.RATE_BY_YEAR:
                return interestRate / 12
            elif interestRateDim == Constants.RATE_BY_DAY:
                return 30 * interestRate
            else:
                return interestRate
        elif periodDim == Constants.PERIOD_BY_DAY:
            if interestRateDim == Constants.RATE_BY_YEAR:
                return interestRate / 365
            elif interestRateDim == Constants.RATE_BY_MONTH:
                return interestRate / 30
            else:
                return interestRate

    @staticmethod
    def calcFuncsReg(capital, interestRate, interestRateDim, period, periodDim, calcType):
        funcs = {
            Constants.CALC_BY_SINGLE_RATE: CalcFunctionUtils.calcFixCapitalSimpleInterest,
            Constants.CALC_BY_PERIOD_SINGLE_RATE: CalcFunctionUtils.calcIncreCapitalSimpleInterest,
            Constants.CALC_BY_COMPOUND_RATE: CalcFunctionUtils.calcFixCapitalCompoundedInterest,
            Constants.CALC_BY_PERIOD_COMPOUND_RATE: CalcFunctionUtils.calcIncreCapitalCompoundedInterest,
            Constants.CALC_BY_YEAR_TO_MONTH_RATE: CalcFunctionUtils.calcAnnualToMonthInterest,
            Constants.CALC_BY_MONTH_TO_YEAR_RATE: CalcFunctionUtils.calcMonthToAnnualInterest
        }
        method = funcs.get(calcType)
        if method:
            interestRate = CalcFunctionUtils.rateConvert(interestRate, interestRateDim, periodDim)
            return method(capital, interestRate, period)
        return [0.0, 0.0, 0.0]

    @staticmethod
    def calcResult(capital, interestRate, interestRateDim, period, periodDim, calcType):
        return CalcFunctionUtils.calcFuncsReg(capital, interestRate, interestRateDim, period, periodDim, calcType)

    @staticmethod
    def detailsFixCapitalSimpleInterest(capital, interestRate, period, startDate=None):
        """单利定存详细内容"""
        result = list()
        capitalMoney = 0
        interestMoney = 0
        capitalInterestMoney = 0
        lastInterestMoney = 0
        for pd in xrange(1, period + 1):
            lastInterestMoney += interestMoney
            capitalMoney = capital
            interestMoney = capitalMoney * interestRate
            capitalInterestMoney = capitalMoney + interestMoney + lastInterestMoney
            result.append(Constants.TEMPLATE2.format(pd, capitalMoney, interestMoney, capitalInterestMoney))
        return result

    @staticmethod
    def detailsIncreCapitalSimpleInterest(capital, interestRate, period, startDate=None):
        """单利每期定存详细内容"""
        result = list()
        capitalMoney = 0
        interestMoney = 0
        capitalInterestMoney = 0
        lastInterestMoney = 0
        for pd in xrange(1, period + 1):
            lastInterestMoney += interestMoney
            capitalMoney += capital
            interestMoney = capitalMoney * interestRate
            capitalInterestMoney = capitalMoney + interestMoney + lastInterestMoney
            result.append(Constants.TEMPLATE2.format(pd, capitalMoney, interestMoney, capitalInterestMoney))
        return result

    @staticmethod
    def detailsFixCapitalCompoundedInterest(capital, interestRate, period, startDate=None):
        """复利定存详细内容"""
        result = list()
        capitalMoney = 0
        interestMoney = 0
        capitalInterestMoney = 0
        for pd in xrange(1, period + 1):
            capitalMoney = capital
            interestMoney = capitalMoney * pow(1 + interestRate, pd) - capitalMoney
            capitalInterestMoney = capitalMoney + interestMoney
            result.append(Constants.TEMPLATE2.format(pd, capitalMoney, interestMoney, capitalInterestMoney))
        return result

    @staticmethod
    def detailsIncreCapitalCompoundedInterest(capital, interestRate, period, startDate=None):
        """复利每期定存详细内容"""
        result = list()
        capitalMoney = 0
        interestMoney = 0
        capitalInterestMoney = 0
        for pd in xrange(1, period + 1):
            capitalMoney += capital
            interestMoney = capital * ((1 + interestRate) / interestRate) * (
                    pow(1 + interestRate, pd) - 1) - capitalMoney
            capitalInterestMoney = capitalMoney + interestMoney
            result.append(Constants.TEMPLATE2.format(pd, capitalMoney, interestMoney, capitalInterestMoney))
        return result

    @staticmethod
    def detailsAnnualToMonthInterest(capital, interestRate, period, startDate=None):
        """单利定存详细内容"""
        pass

    @staticmethod
    def detailsMonthToAnnualInterest(capital, interestRate, period, startDate=None):
        """单利定存详细内容"""
        pass

    @staticmethod
    def detailsFuncsReg(capital, interestRate, interestRateDim, period, periodDim, calcType, startDate=None):
        detailsFuncs = {
            Constants.CALC_BY_SINGLE_RATE: CalcFunctionUtils.detailsFixCapitalSimpleInterest,
            Constants.CALC_BY_PERIOD_SINGLE_RATE: CalcFunctionUtils.detailsIncreCapitalSimpleInterest,
            Constants.CALC_BY_COMPOUND_RATE: CalcFunctionUtils.detailsFixCapitalCompoundedInterest,
            Constants.CALC_BY_PERIOD_COMPOUND_RATE: CalcFunctionUtils.detailsIncreCapitalCompoundedInterest,
            Constants.CALC_BY_YEAR_TO_MONTH_RATE: CalcFunctionUtils.detailsAnnualToMonthInterest,
            Constants.CALC_BY_MONTH_TO_YEAR_RATE: CalcFunctionUtils.detailsMonthToAnnualInterest
        }
        res = list()
        method = detailsFuncs.get(calcType)
        if method:
            interestRate = CalcFunctionUtils.rateConvert(interestRate, interestRateDim, periodDim)
            res.append(Constants.TEMPLATE1.format(periodDim, interestRate))
            res.extend(method(capital, interestRate, period))
        return res

    @staticmethod
    def printDetails(capital, interestRate, interestRateDim, period, periodDim, calcType, startDate=None):
        return CalcFunctionUtils.detailsFuncsReg(capital, interestRate, interestRateDim, period, periodDim, calcType,
                                                 startDate=None)
