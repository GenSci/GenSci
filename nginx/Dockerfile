###################################################################
# NGINX Container Building Script
# This file runs the few commands required to properly spin up the Nginx web
# server container used to serve up the GenSci web app.
####################################################################

FROM nginx:latest
RUN rm -f -- /etc/nginx/sites-enabled/default
RUN mv /etc/nginx/conf.d/default.conf /etc/nginx/conf.d/default.conf.old
RUN mv /etc/nginx/nginx.conf /etc/nginx/nginx.conf.old

ADD sites-enabled/nginx.conf /etc/nginx/nginx.conf
# RUN mkdir /home/logs
# ADD ./logs /home/logs
