# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     maintain_bluesprints.py
# Description:  TODO
# Author:       ckf10000
# CreateDate:   2024/04/03 02:21:02
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
from flask import Blueprint

from apps.common.http.restfulApi import api_factory, anonymous_namespace_prefix
from apps.application.controllers.maintain_controllers import HealthStatusController, UrlMapController, UrlsController

main_blue_name = "main"
main_bp = Blueprint(main_blue_name, __name__)

# 后端调用需要token认证，前端调用需要session认证，none为不加前缀，不认证，anonymous为不认证
main_none_api = api_factory(blueprint=main_bp, prefix=anonymous_namespace_prefix)

# 健康检查
main_none_api.add_resource(HealthStatusController, '/health/getStatus', endpoint='HealthStatusController')
# 当前服务所有的url摘要信息
main_none_api.add_resource(UrlMapController, '/url/getBrief', endpoint='UrlMapController')
# 当前服务所有的url
main_none_api.add_resource(UrlsController, '/url/getAll', endpoint='UrlsController')



