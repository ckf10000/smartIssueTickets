# -*- coding: utf-8 -*-
"""
# -----------------------------------------------------------------------------------------------------------------------
# ProjectName:  smartIssueTickets
# FileName:     app.py
# Description:  TODO
# Author:       ckf10000
# CreateDate:   2024/04/02 15:26:05
# Copyright ©2011-2024. Hunan xyz Company limited. All rights reserved.
# -----------------------------------------------------------------------------------------------------------------------
"""
import platform

if "Windows" not in platform.system():
    import gevent.monkey
    gevent.monkey.patch_all()

if __name__ == '__main__':
    from apps.init_app import flask_app

    if "Windows" in platform.system():
        flask_app.run(host="0.0.0.0", port=5051, threaded=True, load_dotenv=False)
    else:
        from apps.common.http.wsgi import StandaloneApplication

        options = {
            'bind': '%s:%d' % ('0.0.0.0', 5051),
            'loglevel': "debug",  # 全局日志输出的级别， 包括gunicorn框架日志 和 flask业务模块日志
            'logger_enable': False,  # 是否开启gunicorn框架日志记录， 一般情况下无需开启
            'accesslog': 'gunicorn_acess.log',  # 若开启gunicorn框架日志记录， 则访问日志输出到此文件
            'errorlog': 'gunicorn_run.log'  # 若开启gunicorn框架日志记录， 则运行日志输出到此文件
        }
        StandaloneApplication(app=flask_app, options=options).run()
