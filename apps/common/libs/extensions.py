# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     extensions.py
# Description:  TODO
# Author:       ckf10000
# CreateDate:   2024/04/02 15:33:04
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""

import os
from flasgger import Flasgger
from multiprocessing.pool import ThreadPool
from concurrent.futures import ThreadPoolExecutor

from apps.common.libs.dir import get_project_path
from apps.common.http.restfulApi import front_api_namespace_prefix, anonymous_namespace_prefix

pool = ThreadPool(processes=10)
executor = ThreadPoolExecutor(100)

swagger = Flasgger(merge=True, config=dict(specs_route=f"/apidocs/get",
                                           static_url_path="/apidocs/flasgger_static",
                                           url_prefix=f"/{front_api_namespace_prefix}" if os.getenv("ENV_TYPE") in [
                                               "production", "sit", "pre", "uat"] else f"/{anonymous_namespace_prefix}",
                                           specs=[
                                               {
                                                   "endpoint": 'swagger-template',
                                                   "route": '/apidocs/swagger-template.yaml',
                                                   "rule_filter": lambda rule: True,  # all in
                                                   "model_filter": lambda tag: True,  # all in
                                               }
                                           ]),
                   template_file=f"{get_project_path()}/configuration/swagger.yaml")
