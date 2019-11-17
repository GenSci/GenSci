"""
Define Gunciron Configuration.
---------------------------------------
 This file describes the parameters used to configure the gunicorn
 web server which will handle passing requests between the NGINX
 proxy server and the Django application.
"""

import multiprocessing

bind = "127.0.0.1:9000"
errorlog = "-"
accesslog = "-"
reload = True
loglevel = "debug"
workers = multiprocessing.cpu_count() * 2 + 1
timeout = 60 * 10
graceful_timeout = 60 * 5
