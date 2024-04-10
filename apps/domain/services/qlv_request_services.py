# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     qlv_request_services.py
# Description:  TODO
# Author:       ckf10000
# CreateDate:   2024/04/10 13:29:25
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
import typing as t

from apps.common.libs.utils import encryp_md5
from apps.infrastructure.api.http_client import HttpService

class OrderService(object):

    def __init__(self, domain: str, protocol: str) -> None:
        self.__http_client = HttpService(domain=domain, protocol=protocol)

    @classmethod
    def __gen_sign_key(cls, user_key: str, request_data: t.Dict) -> str:
        # 对字典按照键进行排序
        sorted_keys = sorted(request_data.keys())
        result = []
        for key in sorted_keys:
            value = request_data[key]
            if value == "":
                result.append("{}=".format(key))  # 当值为空串时，使用 key=
            else:
                result.append("{}={}".format(key, value))  # 当值不为空串时，使用 key=value
        result.append(user_key)
        # 使用空格连接所有拼接结果
        concatenated_string = "".join(result)
        return encryp_md5(concatenated_string)

    def lock_order(
        self,
        path: str,
        method: str,
        user_key: str,
        user_id: int,
        policy_name: str,
        oper: str,
        air_cos: str = None,
        order_pk: str = None,
        order_src_cat: str = None
    ) -> t.Dict:
        """
        订单锁定
        :params path str: 接口路径
        :params method str: 请求方法
        :params user_key str: 劲旅系统认证用户key
        :params user_id str: 劲旅系统认证用户id
        :params policy_name str: 政策名称关键字
        :params oper str: 操作锁单人，机器人名称
        :params air_cos str: 航司
        :params order_pk str: 劲旅订单号，指定订单号锁单
        :params order_src_cat str: 订单类别，国内/国际
        return t.Dict
        """
        requestData = {
                "policyName": policy_name,
                "airCos": air_cos or "",
                "orderPK": order_pk or "",
                "orderSrcCat": order_src_cat or "",
                "oper": oper
        }
        sign_key = self.__gen_sign_key(user_key=user_key, request_data=requestData)
        json = {
            "UserId": user_id,
            "SignKey": sign_key,
            "requestData": requestData,
        }
        return self.__http_client.send_request(method=method, path=path, json=json)

    def unlock_order(
        self,
        path: str,
        method: str,
        user_key: str,
        user_id: int,
        order_id: int,
        oper: str,
        order_state: str,
        order_lose_type: str,
        remark: str = None
    ) -> t.Dict:
        """
        订单解锁
        :params path str: 接口路径
        :params method str: 请求方法
        :params user_key str: 劲旅系统认证用户key
        :params user_id str: 劲旅系统认证用户id
        :params order_id str: 劲旅系统订单号
        :params oper str: 操作人,机器人名称
        :params order_state str: 出票状态，0:出票失败,1出票成功
        :params order_lose_type str: 出票失败类别，户自定义失败类别,比如:政策,系统等等
        :params remark str: 备注，例如：价格不符
        return t.Dict
        """
        requestData = {
            "orderID": order_id,
            "oper": oper,
            "remark": remark or "",
            "orderState": order_state,
            "orderLoseType": order_lose_type,
        }
        sign_key = self.__gen_sign_key(user_key=user_key, request_data=requestData)
        json = {
            "UserId": user_id,
            "SignKey": sign_key,
            "requestData": requestData,
        }
        return self.__http_client.send_request(method=method, path=path, json=json)

    def write_order_log_new(
        self,
        path: str,
        method: str,
        user_key: str,
        user_id: int,
        order_id: int,
        oper: str,
        logs: str
    ) -> t.Dict:
        """
        订单日志回写
        :params path str: 接口路径
        :params method str: 请求方法
        :params user_key str: 劲旅系统认证用户key
        :params user_id str: 劲旅系统认证用户id
        :params order_id str: 劲旅系统订单号
        :params oper str: 操作人,机器人名称
        :params logs str: 日志内容
        return t.Dict
        """
        requestData = {
            "orderID": order_id,
            "oper": oper,
            "logs": logs
        }
        sign_key = self.__gen_sign_key(user_key=user_key, request_data=requestData)
        json = {
            "UserId": user_id,
            "SignKey": sign_key,
            "requestData": requestData,
        }
        return self.__http_client.send_request(method=method, path=path, json=json)

    def save_order_pay_info(
        self,
        path: str,
        method: str,
        user_key: str,
        user_id: int,
        order_id: int,
        oper: str,
        pay_time: str,
        out_pf: str,
        out_ticket_account: str,
        pay_account_type: str,
        pay_account: str,
        money: str,
        serial_number: str,
        air_co_order_id: str,
        pnames: str,
        d_type: int,
        remark: str = None
    ) -> t.Dict:
        """
        采购信息回填
        :params path str: 接口路径
        :params method str: 请求方法
        :params user_key str: 劲旅系统认证用户key
        :params user_id str: 劲旅系统认证用户id
        :params order_id str: 劲旅系统订单号
        :params oper str: 操作人,机器人名称
        :params pay_time str: 支付时间
        :params out_pf str: 出票平台
        :params out_ticket_account str: 出票账号
        :params pay_account_type str: 支付账号类型
        :params pay_account str: 支付账号
        :params money str: 金额
        :params serial_number str: 流水号
        :params air_co_order_id str: 官网订单号
        :params pnames str: 乘机人姓名
        :params d_type int: 类型，1支付单程,2支付往返,3支付多程
        :params remark str: 备注说明
        return t.Dict
        """
        requestData = {
            "orderID": order_id,
            "payTime": pay_time,
            "outPF": out_pf,
            "outTicketAccount":out_ticket_account,
            "payAccountType": pay_account_type,
            "payAccount": pay_account,
            "money": money,
            "serialNumber": serial_number,
            "airCoOrderID": air_co_order_id,
            "pnames": pnames,
            "oper": oper,
            "remark": remark,
            "type": d_type,
        }
        sign_key = self.__gen_sign_key(user_key=user_key, request_data=requestData)
        json = {
            "UserId": user_id,
            "SignKey": sign_key,
            "requestData": requestData,
        }
        return self.__http_client.send_request(method=method, path=path, json=json)
    
    def fill_order_itinerary_info(
        self,
        path: str,
        method: str,
        user_key: str,
        user_id: int,
        order_id: int,
        oper: str,
        ticket_infos: str
    ) -> t.Dict:
        """
        订单票号回填
        :params path str: 接口路径
        :params method str: 请求方法
        :params user_key str: 劲旅系统认证用户key
        :params user_id str: 劲旅系统认证用户id
        :params order_id str: 劲旅系统订单号
        :params oper str: 操作人,机器人名称
        :params ticket_infos str: 乘机人票号信息，格式如：乘机人1#证件号1#票号1#起飞#到达;乘机人2#证件号2#票号2#起飞#到达
        return t.Dict
        """
        requestData = {
            "orderID": order_id,
            "oper": oper,
            "ticketInfos": ticket_infos
        }
        sign_key = self.__gen_sign_key(user_key=user_key, request_data=requestData)
        json = {
            "UserId": user_id,
            "SignKey": sign_key,
            "requestData": requestData,
        }
        return self.__http_client.send_request(method=method, path=path, json=json)
