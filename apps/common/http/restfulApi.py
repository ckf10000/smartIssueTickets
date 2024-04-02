# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     restfulApi.py
# Description:  TODO
# Author:       ckf10000
# CreateDate:   2024/04/02 12:05:34
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""

import sys
from flask_restful import Api
from flask import current_app, Blueprint
from werkzeug.datastructures import Headers
from werkzeug.exceptions import HTTPException
from flask.signals import got_request_exception
from flask_restful.utils import http_status_message


class RestfulApi(Api):

    def handle_error(self, e):
        """
        自定义异常抛出类型
        :param object e: the raised Exception object
        """
        got_request_exception.send(current_app, exception=e)

        if not isinstance(e, HTTPException) and current_app.propagate_exceptions:
            exc_type, exc_value, tb = sys.exc_info()
            if exc_value is e:
                raise
            else:
                raise e

        headers = Headers()
        if isinstance(e, HTTPException):
            if e.response is not None:
                resp = e.get_response()
                return resp

            code = e.code
            default_data = {'code': code,
                            'message': getattr(e, 'description', http_status_message(code)),
                            'data': None
                            }
            headers = e.get_response().headers
        else:
            code = 500
            default_data = {'code': code,
                            'message': http_status_message(code),
                            'data': None
                            }

        remove_headers = ('Content-Length',)

        for header in remove_headers:
            headers.pop(header, None)

        try:
            message_dict = getattr(e, 'data')
            message = message_dict.get("message")
            data = {"code": e.code,
                    "message": list(message.values())[0] if isinstance(message, dict) and len(
                        message) == 1 else message,
                    'data': None}
        except AttributeError:
            data = default_data

        if code and code >= 500:
            exc_info = sys.exc_info()
            if exc_info[1] is None:
                exc_info = None
            current_app.log_exception(exc_info)

        error_cls_name = type(e).__name__
        if error_cls_name in self.errors:
            custom_data = self.errors.get(error_cls_name, {})
            code = custom_data.get('status', 500)
            data.update(custom_data)

        if code == 406 and self.default_mediatype is None:
            supported_media_types = list(self.representations.keys())
            fallback_media_type = supported_media_types[0] if supported_media_types else "text/plain"
            resp = self.make_response(
                data,
                code,
                headers,
                fallback_mediatype=fallback_media_type
            )
        else:
            resp = self.make_response(data, code, headers)

        if code == 401:
            resp = self.unauthorized(resp)
        return resp

    def _complete_url(self, url_part, registration_prefix):
        """This method is used to defer the construction of the final url in
        the case that the Api is created with a Blueprint.

        :param url_part: The part of the url the endpoint is registered with
        :param registration_prefix: The part of the url contributed by the
            blueprint.  Generally speaking, BlueprintSetupState.url_prefix
        """
        if self.prefix.find(",") != -1:
            parts = [dict(b=registration_prefix, a=x, e=url_part) for x in self.prefix.split(",")]
        else:
            parts = {
                'b': registration_prefix,
                'a': self.prefix,
                'e': url_part
            }
        if isinstance(parts, dict):
            urls = ''.join(parts[key] for key in self.url_part_order if parts[key])
        else:
            urls = list()
            for part in parts:
                urls.append(''.join(part[key] for key in self.url_part_order if part[key]))
        return urls


def api_factory(blueprint: Blueprint, prefix: str = '', decorators=None, url_part_order: str = 'bae') -> Api:
    """
    api工厂
    :param object blueprint: 蓝本
    :param str or list prefix: 路由关键字
    :param str url_part_order:  默认"bae"，parts = {
                                                    'b': registration_prefix,  # register_blueprint 的 url_prefix
                                                    'a': self.prefix,
                                                    'e': url_part
                                                }
    :param list decorators: 装饰器列表  例如：[check_http_headers, check_request_frequency]
    :return: api对象
    """
    if prefix:
        prefix = ",".join([f"/{x}" for x in prefix]) if isinstance(prefix, list) else f"/{prefix}"
        api = RestfulApi(app=blueprint, prefix=prefix)
        url_part_order = "abe"
    else:
        api = RestfulApi(app=blueprint)
    api.url_part_order = url_part_order
    api.catch_all_404s = False
    api.serve_challenge_on_401 = False
    api.decorators = decorators if decorators else []
    return api


end_api_namespace_prefix = "/rest/api"
anonymous_namespace_prefix = "/open/api"
front_api_namespace_prefix = "/internal/api"
