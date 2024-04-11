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
from multiprocessing.pool import ThreadPool
from concurrent.futures import ThreadPoolExecutor


pool = ThreadPool(processes=10)
executor = ThreadPoolExecutor(100)
