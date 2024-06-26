# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     http_client.py
# Description:  TODO
# Author:       ckf10000
# CreateDate:   2024/04/10 13:22:18
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
import requests
import typing as t
from apps.common.annotation.log_service import logger
from apps.common.libs.utils import covert_dict_key_to_lower, get_html_title


class HttpService(object):
    __time_out = 10
    __domain = None
    __url = None
    __protocol = None
    __headers = t.Dict = {
        "Content-Type": "application/json; charset=UTF-8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) " +
                      "Chrome/123.0.0.0 Safari/537.36"
    }

    def __init__(self, domain: str, protocol: str) -> None:
        self.__domain = domain
        self.__protocol = protocol

    def send_request(self, method: str, path: str, params: t.Dict = None, data: t.Dict = None, json: t.Dict = None,
                     headers: t.Dict = None) -> t.Dict:
        if isinstance(headers, dict):
            self.__headers = headers
        self.__url = "{}://{}{}".format(self.__protocol, self.__domain, path)
        # 发送HTTP请求
        logger.info(
            "开始发起http请求，url: {}, 方法：{}，请求params参数：{}，请求headers参数：{}，请求data参数：{}，请求json参数：{}".format(
                self.__url,
                method,
                params or "{}",
                self.__headers,
                data or "{}",
                json or "{}",
            )
        )
        return self.__send_http_request(method=method, params=params, data=data, json=json)

    def __send_http_request(self, method: str, params: t.Dict = None, data: t.Dict = None,
                            json: t.Dict = None) -> t.Dict:
        # 实际发送HTTP请求的内部方法
        # 使用 requests 库发送请求
        method = method.lower().strip()
        if method in ("get", "post"):
            try:
                if method == "get":
                    response = requests.get(self.__url, params=params, verify=False, timeout=self.__time_out,
                                            headers=self.__headers)
                else:
                    response = requests.post(self.__url, params=params, json=json, data=data, verify=False,
                                             timeout=self.__time_out, headers=self.__headers)
                result = self.__parse_data_response(response=response)
            except Exception as e:
                logger.error("调用url<{}>异常，原因：{}".format(self.__url, str(e)))
                result = dict(code=500, message=str(e), data=dict())
        else:
            result = dict(code=400, message="Unsupported HTTP method: {}".format(
                method), data=dict())
        return result

    def __parse_data_response(self, response: requests.Response) -> t.Dict:
        # 获取 Content-Type 头信息
        content_type = response.headers.get('Content-Type')
        # 判断返回的内容类型
        if 'application/json' in content_type or 'text/json' in content_type:
            # JSON 类型
            data = covert_dict_key_to_lower(d=response.json())
        elif 'text/plain' in content_type:
            # 纯文本类型
            data = dict(code=response.status_code, message=get_html_title(
                html=response.text), data=response.text)
        else:
            # 其他类型，默认视为二进制内容
            content = response.content.decode('utf-8')
            data = dict(code=response.status_code,
                        message=get_html_title(html=content), data=content)
        logger.info("调用url: {}的正常返回值为：{}".format(self.__url, data))
        return data
