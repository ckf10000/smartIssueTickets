# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     element.py
# Description:  TODO
# Author:       ckf10000
# CreateDate:   2024/04/06 03:04:22
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
import re
import typing as t
from decimal import Decimal
# from apps.common.libs.utils import get_ui_object_proxy_attr
from poco.drivers.android.uiautomation import AndroidUiautomationPoco

class CtripAppOrderElementConverter(object):

    @classmethod
    def extract_ctrip_order_page_poco_as_list(cls, poco: AndroidUiautomationPoco) -> t.Union[AndroidUiautomationPoco]:
        poco_list = list()
        for child_1 in poco.children():
            for child_2 in child_1.children():
                poco_2_name = child_2.get_name()
                if re.search("^\d+.*", poco_2_name) is not None:
                    for child_3 in child_2.children():
                        poco_3_name = child_3.get_name()
                        if re.search("^\d+.*", poco_3_name) is not None:
                            poco_list.append(child_3)
        return poco_list

    @classmethod
    def ctrip_order_element_as_dict(cls, poco_list: t.Union[AndroidUiautomationPoco]) -> t.Dict:
        orders_dict = dict()
        for poco in poco_list:
            view_id = poco.get_name().strip()
            order_dict = dict()
            for child in poco.children():
                z_orders = child.attr("zOrders")
                if z_orders.get("local") == 1:
                    departure_city_poco = child.children()[0]
                    departure_city_name = departure_city_poco.get_text().strip()
                    order_dict["departure_city_name"] = departure_city_name
                elif z_orders.get("local") == 3:
                    arrive_city_poco = child.children()[0]
                    arrive_city_name = arrive_city_poco.get_text().strip()
                    order_dict["arrive_city_name"] = arrive_city_name
                elif z_orders.get("local") == 4:
                    text_slice = child.get_text().split("至")
                    order_dict["departure_time"] = text_slice[0].strip()
                    order_dict["arrive_time"] = text_slice[-1].strip()
                elif z_orders.get("local") == 5:
                    text_slice = child.get_text().split(" ")
                    order_dict["flight"] = text_slice[0].strip()
                elif z_orders.get("local") == 6:
                    order_price_poco = child.children()[0]
                    order_price = order_price_poco.get_text().strip()
                    order_dict["order_price"] = Decimal(order_price[1:])
            if order_dict:
                order_dict['view_id'] = view_id
                orders_dict[view_id] = order_dict
        return orders_dict
