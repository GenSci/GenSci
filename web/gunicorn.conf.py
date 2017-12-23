"""
Gunicorn Configuration File:
---------------------------------
 This file describes the parameters used to configure the gunicorn web server which will handle passing requests between the NGINX proxy server and the Django application.
"""

bind="127.0.0.1:9000"
errorlog = '/var/log/gunicorn/gunicorn-error.log'
accesslog = '/var/log/gunicorn/gunicorn-access.log'
reload = True
loglevel='debug'
workers = 5
timeout = 60*10
graceful_timeout = 60*5
