# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     wsgi.py
# Description:  TODO
# Author:       ckf10000
# CreateDate:   2024/04/02 12:07:52
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""

import os
import traceback
import multiprocessing
from pathlib import Path
from gunicorn.app.base import BaseApplication

from apps.common.libs.dir import get_project_path
from apps.common.annotation.log_service import auto_log, logger
from apps.common.libs.parse_yaml import DictObject, ProjectConfig


class Config:
    @classmethod
    def query_cpu(cls):
        avail_cpu = 0
        if os.path.isfile('/sys/fs/cgroup/cpu/cpu.cfs_quota_us'):
            cpu_quota = int(open('/sys/fs/cgroup/cpu/cpu.cfs_quota_us').read().rstrip())
            # 如果是 -1，则为物理主机，否则就是k8s容器虚拟主机
            if cpu_quota != -1 and os.path.isfile('/sys/fs/cgroup/cpu/cpu.cfs_period_us'):
                cpu_period = int(open('/sys/fs/cgroup/cpu/cpu.cfs_period_us').read().rstrip())
                avail_cpu = int(cpu_quota / cpu_period)
            # elif os.path.isfile('/sys/fs/cgroup/cpu/cpu.shares'):
            #     cpu_shares = int(open('/sys/fs/cgroup/cpu/cpu.shares').read().rstrip())
            #     avail_cpu = int(cpu_shares / 1024)
        return avail_cpu

    @classmethod
    def number_of_workers(cls):
        avail_cpu = cls.query_cpu()
        if avail_cpu > 0:
            return (int(avail_cpu) * 2) + 1
        else:
            return (multiprocessing.cpu_count() * 2) + 1

    @classmethod
    def worker_default(cls) -> dict:
        config_default = dict(
            threads=5,
            # 监听地址和端口
            bind="0.0.0.0:5051",
            # 服务器中在pending状态的最大连接数，即client处于waiting的数目。
            # 超过这个数目， client连接会得到一个error。建议值64-2048。
            backlog=64,
            # 设置守护进程,应用是否以daemon方式运行
            daemon=False,
            # 当代码有修改时，自动重启workers。适用于开发环境
            reload=False,
            # worker重启之前处理的最大requests数， 缺省值为0表示自动重启disabled。主要是防止内存泄露。
            max_requests=0,
            # 通常设为30
            timeout=30,
            # server端保持连接时间
            keepalive=300,
            # worker进程的工作方式。 有sync, eventlet, gevent, tornado, gthread, 缺省值sync。
            worker_class="gevent",
            # 设置最大并发量
            worker_connections=2000
        )
        return DictObject(config_default)

    @classmethod
    def get_dict(cls, options=None):
        try:
            config = getattr(ProjectConfig.get_object(), "gunicorn")
            if config.logger_enable is False:
                config["errorlog"] = None
                config["accesslog"] = None
            else:
                if "errorlog" in config.keys():
                    config['errorlog'] = str(Path(get_project_path(), "logs", config.get('errorlog')))
                if "accesslog" in config.keys():
                    config['accesslog'] = str(Path(get_project_path(), "logs", config.get('accesslog')))
        except Exception as e:
            logger.error(e)
            logger.error(traceback.format_exc())
            config = Config.worker_default()
            if options:
                if options.get("logger_enable") is False:
                    options["errorlog"] = None
                    options["accesslog"] = None
                else:
                    if "errorlog" in options.keys():
                        options['errorlog'] = str(Path(get_project_path(), "logs", options.get('errorlog')))
                    if "accesslog" in options.keys():
                        options['accesslog'] = str(Path(get_project_path(), "logs", options.get('accesslog')))
                config.update(options)
        config.update(**dict(workers=Config.number_of_workers()))
        return config


class StandaloneApplication(BaseApplication):

    def __init__(self, app, options=None):
        self.application = app
        self.options = options or dict()
        super().__init__()

    @auto_log
    def load_config(self):
        conf = Config.get_dict(self.options)
        config = {key: value for key, value in conf.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

    def init(self, parser, opts, args):
        raise NotImplementedError