# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     base_controller.py
# Description:  TODO
# Author:       ckf10000
# CreateDate:   2024/04/02 11:59:25
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""

from flask import request, g
from flask_restful import Resource, reqparse


class CustomRequestParser(reqparse.RequestParser):

    def parse_args(self, *args, **kwargs):
        # 检查请求参数类型是否为 'params'、'json',为了兼容，不传递参数时，报错：
        # werkzeug.exceptions.UnsupportedMediaType: 415 Unsupported Media Type: Did not attempt to load JSON data because the request Content-Type was not 'application/json'
        if request.args or request.get_json(silent=True):
            # 如果请求中存在 'params'、'json'参数，则解析请求参数
            return super().parse_args(*args, **kwargs)
        else:
            # 如果请求中不存在任何参数，则返回空字典
            return {}


class BaseController(Resource):

    def __init__(self):
        super().__init__()
        self.__env = request.headers.environ
        self.origin = (
            self.__env.get("HTTP_ORIGIN").split("//")[1]
            if self.__env.get("HTTP_ORIGIN")
            else None
        )
        self.forwarded_for = (
            self.__env.get("HTTP_X_FORWARDED_FOR").split(",")[0]
            if self.__env.get("HTTP_X_FORWARDED_FOR")
            else None
        )
        self.remote_ip = (
            self.forwarded_for
            if self.forwarded_for
            else self.__env.get("REMOTE_ADDR").split(",")[0]
        )
        self.remote_port = self.__env.get("REMOTE_PORT")
        self.method = self.__env.get("REQUEST_METHOD")
        self.url = request.url
        self.access_user = request.remote_user
        self.current_login_user = getattr(g, "user_key", None)

        if self.access_user:
            if self.origin:
                self.logger_formatter = (
                    "来自域名：<{}>的转发主机".format(self.origin)
                    + "IP：<{}>".format(self.remote_ip)
                    + "的端口：[{}]的 {} 用户".format(
                        self.remote_port, self.access_user
                    )
                    + "通过 {} ".format(self.method)
                    + "方法访问url：{}".format(self.url)
                )
            else:
                self.logger_formatter = (
                    "来自主机IP：<{}>".format(self.remote_ip)
                    + "的端口：[{}]的 {} 用户".format(
                        self.remote_port, self.access_user
                    )
                    + "通过 {} ".format(self.method)
                    + "方法访问url：{}".format(self.url)
                )
        else:
            if self.origin:
                self.logger_formatter = (
                    "来自域名：<{}>的转发主机".format(self.origin)
                    + "IP：<{}>".format(self.remote_ip)
                    + "的端口：[{}]".format(self.remote_port)
                    + "通过 {} ".format(self.method)
                    + "方法访问url：{}".format(self.url)
                )
            else:
                self.logger_formatter = (
                    "来自主机IP：<{}>".format(self.remote_ip) + "的端口：[{}]".format(self.remote_port) + "通过 {} ".format(self.method) + "方法访问url：{}".format(self.url)
                    )


class BaseArgumentController(BaseController):

    def __init__(self):
        super().__init__()
        # 获取请求参数, bundle_errors: 错误捆绑在一起并立即发送回客户端
        self.parse = CustomRequestParser(bundle_errors=True)
