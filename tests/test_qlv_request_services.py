# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     test_qlv_request_services.py
# Description:  TODO
# Author:       ckf10000
# CreateDate:   2024/04/10 14:03:37
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
from apps.domain.services.qlv_request_services import OrderService

protocol="http"
domain="outsideapi.qlv88.com"

def test_lock_order():
    kwargs = {
        "path": "/LockOrder.ashx",
        "method": "post",
        "user_key": "9a68295ec90b1fc10ab94331c882bab9",
        "user_id": 186,
        "policy_name": "测试-XC",
        "oper": "robot-XC",
        "air_cos": "",
        "order_pk": "",
        "order_src_cat": "国内"
    }
    OrderService(domain=domain, protocol=protocol).lock_order(**kwargs)

def test_unlock_order():
    kwargs = {
        "path": "/OrderUnlock.ashx",
        "method": "post",
        "user_key": "9a68295ec90b1fc10ab94331c882bab9",
        "user_id": 186,
        "order_id": 1234567890,
        "oper": "robot-XC",
        "order_state": "0",
        "order_lose_type": "政策",
        "remark": "价格不符"
    }
    OrderService(domain=domain, protocol=protocol).unlock_order(**kwargs)

def test_write_order_log_new():
    kwargs = {
        "path": "/OrderLogWriteNew.ashx",
        "method": "post",
        "user_key": "9a68295ec90b1fc10ab94331c882bab9",
        "user_id": 186,
        "order_id": 1234567890,
        "oper": "robot-XC",
        "logs": "这是一条测试日志"
    }
    OrderService(domain=domain, protocol=protocol).write_order_log_new(**kwargs)

def test_save_order_pay_info():
    kwargs = {
        "path": "/OrderPayInfoSave.ashx",
        "method": "post",
        "user_key": "9a68295ec90b1fc10ab94331c882bab9",
        "user_id": 186,
        "order_id": 1232132131231231,
        "pay_time": "2021-07-27 19:46:00",
        "out_pf": "GSB2C",
        "out_ticket_account": "GSB2C",
        "pay_account_type": "易宝",
        "pay_account": "易宝会员",
        "money": 1000,
        "serial_number": "测试123456",
        "air_co_order_id": "测试官网123456",
        "pnames": "徐婷婷,顾欣桐",
        "oper": "rbt测试",
        "remark": "备注",
        "d_type": 1
    }
    OrderService(domain=domain, protocol=protocol).save_order_pay_info(**kwargs)

def test_fill_order_itinerary_info():
    kwargs = {
        "path": "/BackfillTicketNumberNew.ashx",
        "method": "post",
        "user_key": "9a68295ec90b1fc10ab94331c882bab9",
        "user_id": 186,
        "order_id": 1232132131231231,
        "oper": "rbt测试",
        "ticket_infos": "徐婷婷#320922199010249022#100-1010101010#TSN#HAK;顾欣桐#320982201701200021#200-1010101010#TSN#HAK"
    }
    OrderService(domain=domain, protocol=protocol).fill_order_itinerary_info(**kwargs)

if __name__ == "__main__":
    # test_lock_order()
    # test_unlock_order()
    # test_write_order_log_new()    
    # test_save_order_pay_info()
    test_fill_order_itinerary_info()