# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     calc.py
# Description:  TODO
# Author:       ckf10000
# CreateDate:   2024/03/21 23:48:53
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
import re
import typing as t
from traceback import format_exc

def calc_text_equation(text: str) -> str:
    try:
        # 使用正则表达式提取数字和运算符
        matches = re.findall(r'\d+|加|减|乘|除', text)

        # 将中文运算符转换为对应的算术运算符
        for i, match in enumerate(matches):
            if match == "加":
                matches[i] = "+"
            elif match == "减":
                matches[i] = "-"
            elif match == "乘":
                matches[i] = "*"
            elif match == "除":
                matches[i] = "/"

        # 将提取的文本连接成一个字符串并计算结果
        calculation = ''.join(matches)
        result = eval(calculation)
        return str(result)
    except Exception as e:
        format_exc()
        del e
        return text


if __name__ == "__main__":
    r = calc_text_equation(text="89加35等")
    print("计算结果：", r)