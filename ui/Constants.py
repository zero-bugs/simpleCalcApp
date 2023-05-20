#!/usr/bin/python3
# -*- coding: UTF-8 -*-


class Constants:
    # 打印模板
    TEMPLATE1 = "概要: 利率（{}）: {:.4%}"
    TEMPLATE2 = "第{:>d}期|本金:{:.2f}元|利息:{:.2f}元|本息和:{:.2f}元"

    TEMPLATE_SEQ = '|'

    # 时间格式模板
    DATE_TEMPLATE = "yyyy/MM/dd"
    DATE_TEMPLATE_PY = "%Y/%m/%d"
    TIME_TEMPLATE = "%Y/%m/%d HH:mm:ss"

    RATE_BY_YEAR = '年息'
    RATE_BY_MONTH = '月息'
    RATE_BY_DAY = '日息'

    PERIOD_BY_YEAR = '按年'
    PERIOD_BY_MONTH = '按月'
    PERIOD_BY_DAY = '按天'

    CALC_BY_SINGLE_RATE = '单利定存'
    CALC_BY_PERIOD_SINGLE_RATE = '单利每期定存'
    CALC_BY_COMPOUND_RATE = '复利定存'
    CALC_BY_PERIOD_COMPOUND_RATE = '复利每期定存'
    CALC_BY_YEAR_TO_MONTH_RATE = '年息转月息'
    CALC_BY_MONTH_TO_YEAR_RATE = '月息转年息'

    RATE_YEAR_MONTH = 12
    RATE_MONTH_DAY = 30
    RATE_YEAR_DAYS = 360
