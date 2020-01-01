####################################################################
# Django container DockerFile
# This file is used to build the container image, including creating the logs
# for the Gunicorn web server as well as install the requirements defined for
# this application.
####################################################################

FROM python:3.7
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN pip install -r requirements.txt
