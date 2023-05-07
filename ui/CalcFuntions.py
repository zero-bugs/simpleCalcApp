#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from urllib3.connectionpool import xrange


class CalcFunctionUtils:
    template1 = "利率（{}）：{:.4%}"
    template2 = "第{:>d}期\t本金：{:.2f}\t利息：{:.2f}，本息和：{:.2f} 元"

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
        if periodDim == '按年':
            if interestRateDim == '月息':
                return 12 * interestRate
            elif interestRateDim == '日息':
                return 365 * interestRate
            else:
                return interestRate
        elif periodDim == '按月':
            if interestRateDim == '年息':
                return interestRate / 12
            elif interestRateDim == '日息':
                return 30 * interestRate
            else:
                return interestRate
        elif periodDim == '按天':
            if interestRateDim == '年息':
                return 365 * interestRate
            elif interestRateDim == '月息':
                return 30 * interestRate
            else:
                return interestRate

    @staticmethod
    def calcFuncsReg(capital, interestRate, interestRateDim, period, periodDim, calcType):
        funcs = {
            '单利定存': CalcFunctionUtils.calcFixCapitalSimpleInterest,
            '单利每期定存': CalcFunctionUtils.calcIncreCapitalSimpleInterest,
            '复利定存': CalcFunctionUtils.calcFixCapitalCompoundedInterest,
            '复利每期定存': CalcFunctionUtils.calcIncreCapitalCompoundedInterest,
            '年息转月息': CalcFunctionUtils.calcAnnualToMonthInterest,
            '月息转年息': CalcFunctionUtils.calcMonthToAnnualInterest
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
    def detailsFixCapitalSimpleInterest(capital, interestRate, period):
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
            result.append(CalcFunctionUtils.template2.format(pd, capitalMoney, interestMoney, capitalInterestMoney))
        return result

    @staticmethod
    def detailsIncreCapitalSimpleInterest(capital, interestRate, period):
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
            result.append(CalcFunctionUtils.template2.format(pd, capitalMoney, interestMoney, capitalInterestMoney))
        return result

    @staticmethod
    def detailsFixCapitalCompoundedInterest(capital, interestRate, period):
        """复利定存详细内容"""
        result = list()
        capitalMoney = 0
        interestMoney = 0
        capitalInterestMoney = 0
        for pd in xrange(1, period + 1):
            capitalMoney = capital
            interestMoney = capitalMoney * pow(1+interestRate, pd) - capitalMoney
            capitalInterestMoney = capitalMoney + interestMoney
            result.append(CalcFunctionUtils.template2.format(pd, capitalMoney, interestMoney, capitalInterestMoney))
        return result

    @staticmethod
    def detailsIncreCapitalCompoundedInterest(capital, interestRate, period):
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
            result.append(CalcFunctionUtils.template2.format(pd, capitalMoney, interestMoney, capitalInterestMoney))
        return result

    @staticmethod
    def detailsAnnualToMonthInterest(capital, interestRate, period):
        """单利定存详细内容"""
        pass

    @staticmethod
    def detailsMonthToAnnualInterest(capital, interestRate, period):
        """单利定存详细内容"""
        pass

    @staticmethod
    def detailsFuncsReg(capital, interestRate, interestRateDim, period, periodDim, calcType):
        detailsFuncs = {
            '单利定存': CalcFunctionUtils.detailsFixCapitalSimpleInterest,
            '单利每期定存': CalcFunctionUtils.detailsIncreCapitalSimpleInterest,
            '复利定存': CalcFunctionUtils.detailsFixCapitalCompoundedInterest,
            '复利每期定存': CalcFunctionUtils.detailsIncreCapitalCompoundedInterest,
            '年息转月息': CalcFunctionUtils.detailsAnnualToMonthInterest,
            '月息转年息': CalcFunctionUtils.detailsMonthToAnnualInterest
        }
        res = list()
        method = detailsFuncs.get(calcType)
        if method:
            interestRate = CalcFunctionUtils.rateConvert(interestRate, interestRateDim, periodDim)
            res.append(CalcFunctionUtils.template1.format(periodDim, interestRate))
            res.extend(method(capital, interestRate, period))
        return res

    @staticmethod
    def printDetails(capital, interestRate, interestRateDim, period, periodDim, calcType):
        return CalcFunctionUtils.detailsFuncsReg(capital, interestRate, interestRateDim, period, periodDim, calcType)
