# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     date_extend.py
# Description:  日期计算扩展包
# Author:       ckf10000
# CreateDate:   2024/03/26 14:39:32
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
import typing as t
from datetime import datetime, timedelta

flight_standard_date_format = "%Y-%m-%d %H:%M"
standard_date_format = flight_standard_date_format + ":%S"

def get_trip_year_month_day(date_str: str) -> t.Tuple:
    """携程日历界面头部上的选择区域"""
    trip_dt = datetime.strptime(date_str, flight_standard_date_format)
    current_dt = datetime.now()
    if  trip_dt >= current_dt + timedelta(minutes=60):
        year = "{}年".format(trip_dt.year)
        month = "{}月".format(trip_dt.month)
        day = "{}".format(trip_dt.day)
        return year, month, day
    else:
        raise ValueError("航班时间: {} 已失效或接近当前时间: {}".format(date_str, current_dt.strftime(flight_standard_date_format)))
    
    

if __name__ == "__main__":
    print(get_trip_year_month_day(date_str="2024-03-29 11:00"))



