# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     flask_plus.py
# Description:  TODO
# Author:       ckf10000
# CreateDate:   2024/04/02 12:04:31
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
from flask import Flask

try:
    from flask.app import setupmethod
except ImportError:
    from flask.sansio.scaffold import setupmethod

try:
    from flask.helpers import _endpoint_from_view_func
except ImportError:
    from flask.sansio.scaffold import _endpoint_from_view_func


class FlaskPlus(Flask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @setupmethod
    def add_url_rule(
            self,
            rule: str,
            endpoint=None,
            view_func=None,
            provide_automatic_options=None,
            **options
    ) -> None:
        if endpoint is None:
            endpoint = _endpoint_from_view_func(view_func)
        options["endpoint"] = endpoint
        methods = options.pop("methods", None)
        if methods is None:
            methods = getattr(view_func, "methods", None) or ("GET",)
        if isinstance(methods, str):
            raise TypeError(
                "Allowed methods have to be iterables of strings, "
                'for example: @app.route(..., methods=["POST"])'
            )
        methods = set(item.upper() for item in methods)
        required_methods = set(getattr(view_func, "required_methods", ()))
        if provide_automatic_options is None:
            provide_automatic_options = getattr(
                view_func, "provide_automatic_options", None
            )
        if provide_automatic_options is None:
            if "OPTIONS" not in methods:
                provide_automatic_options = True
                required_methods.add("OPTIONS")
            else:
                provide_automatic_options = False
        methods |= required_methods
        rules = list()
        if isinstance(rule, list):
            for x in rule:
                rules.append(self.url_rule_class(x, methods=methods, **options))
        else:
            rules.append(self.url_rule_class(rule, methods=methods, **options))
        for x in rules:
            x.provide_automatic_options = provide_automatic_options
            self.url_map.add(x)
        if view_func is not None:
            old_func = self.view_functions.get(endpoint)
            if old_func is not None and old_func != view_func:
                raise AssertionError(
                    "View function mapping is overwriting an "
                    "existing endpoint function: %s" % endpoint
                )
            self.view_functions[endpoint] = view_func
