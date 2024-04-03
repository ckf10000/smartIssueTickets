# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     maintain_services.py
# Description:  TODO
# Author:       ckf10000
# CreateDate:   2024/04/03 01:59:00
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
import typing as t
from flask import current_app

__all__ = ['main_ser']


class MaintainService(object):

    @classmethod
    def test_service_status(cls) -> t.Dict:
        return dict(code=200, message="测试成功", data=None)
    
    @classmethod
    def get_instances_brief(cls):
        data = [dict(url_suffix=x.rule[1:], is_leaf=x.is_leaf, endpoint=x.endpoint,
                     arguments=list(x.arguments) if x.arguments else None,
                     methods=list(x.methods), websocket=x.websocket) for x in
                current_app.url_map.iter_rules()] if current_app.url_map.iter_rules() else list()
        data.sort(key=lambda d: d.get("url_suffix"), reverse=False)
        return dict(code=200, message='查询成功', data=data)

    @classmethod
    def get_urls(cls):
        data = [x.rule[1:] for x in current_app.url_map.iter_rules()] if current_app.url_map.iter_rules() else list()
        data.sort()
        return dict(code=200, message='查询成功.', data=data)


main_ser = MaintainService()
