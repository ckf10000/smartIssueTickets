# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     init_app.py
# Description:  TODO
# Author:       ckf10000
# CreateDate:   2024/04/02 18:22:28
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
import os
from json import dumps
from flask_cors import CORS
from datetime import datetime
from flask.wrappers import Response
from flask import Flask, g, request
from flask.logging import default_handler

from apps.common.libs.environ import get_env
from apps.common.libs.context import swagger
from apps.common.http.flask_plus import FlaskPlus
from apps.common.libs.dir import get_project_path
from apps.common.libs.service_environ import config
from apps.common.annotation.log_service import logger
from apps.common.http.restfulApi import front_api_namespace_prefix

__all__ = ["flask_app"]


def create_app():
    os.environ["APP_NAME"] = APP_NAME = "smartIssueTickets"
    os.environ["ENV_TYPE"] = get_env()
    os.environ["FLASK_ENV"] = get_env()
    os.environ["PROJECT_HOME"] = get_project_path()
    os.environ["FLASK_DEBUG"] = str(config[get_env()].DEBUG).lower()
    app = FlaskPlus(
        import_name=APP_NAME,
        root_path=get_project_path(),
        static_url_path=f"/{front_api_namespace_prefix}/static",
    )
    app.logger.removeHandler(default_handler)
    register_env(app, get_env())
    register_extensions(app)
    register_blueprints(app)
    register_request_handlers(app)
    register_response_handlers(app=app)
    return app


def register_env(app: Flask, config_name: str):
    app.config.from_object(config[config_name])
    service_constant = getattr(config[config_name].CONFIG, "service_constant")
    app.config.update(service_constant)


def register_extensions(app: Flask):
    if get_env() not in ["production", "pre"]:
        swagger.init_app(app=app)
    # supports_credentials 是否允许请求发送cookie
    CORS(app=app, supports_credentials=True, max_age=600)


def register_blueprints(app: Flask):
    from apps.application.bluesprints.maintain_bluesprints import main_bp
    from apps.application.bluesprints.booking_bluesprints import booking_bp
    app.register_blueprint(main_bp, url_prefix='/' + main_bp.name)
    app.register_blueprint(booking_bp, url_prefix="/" + booking_bp.name)


def register_request_handlers(app: Flask):

    @app.before_request
    def http_request():
        start_time = datetime.now()
        request_method = request.headers.environ.get("REQUEST_METHOD")
        req_kwargs = dict()
        if request.args:
            req_kwargs.update(dict(request.args))
        elif request.get_json(silent=True):
            req_kwargs.update(request.json)
        setattr(g, "request", dict(url=request.url, method=request_method,
                start_time=start_time, req_kwargs=req_kwargs))
        remote_port = request.headers.environ.get("REMOTE_PORT")
        # 前端调用服务端
        origin = (
            request.headers.environ.get("HTTP_ORIGIN").split("//")[1]
            if request.headers.environ.get("HTTP_ORIGIN")
            else None
        )
        forwarded_for = (
            request.headers.environ.get("HTTP_X_FORWARDED_FOR").split(",")[0]
            if request.headers.environ.get("HTTP_X_FORWARDED_FOR")
            else None
        )
        remote_addr = (
            forwarded_for
            if forwarded_for
            else request.headers.environ.get("REMOTE_ADDR").split(",")[0]
        )
        if origin:
            logger.info(
                "来自域名：<{}>的转发主机IP：<{}>的端口：[{}]通过 {} 方法访问url：{}。".format(
                    origin, remote_addr, remote_port, request_method, request.url
                )
            )
        else:
            logger.info(
                "来自主机IP：<{}>的端口：[{}]通过 {} 方法访问url：{}。".format(
                    remote_addr, remote_port, request_method, request.url
                )
            )


def register_response_handlers(app: Flask):
    @app.after_request
    def http_response(response: Response):
        """
        HTTP响应头拦截器，在所有的请求发生后执行，加入headers。
        :param response response: http响应对象
        :return: response对象
        """
        request_id = getattr(g, "request_id", None)
        if request_id:
            data_json = response.get_json()
            if data_json:
                data_json.update(dict(requestId=request_id))
                response.set_data(dumps(data_json))
            response.headers["U-Request-Id"] = request_id
        logger.info(
            f"当前[{g.request.get('method')}]请求: {g.request.get('url')} "
            f"的响应状态(status_code)：{response.status_code}"
        )
        tt = datetime.now() - g.request.get("start_time")
        total_seconds = tt.total_seconds()
        logger.warning(f"当前请求的响应耗时: <{total_seconds}>秒")
        return response


flask_app = create_app()
