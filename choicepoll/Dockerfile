#
# Python Dockerfile
#
# https://github.com/
#

# Pull base image.
FROM python

# Maintained by
MAINTAINER Steve Richards <srichards@leftshiftit.com>

# Install Python.
RUN \
 apt-get update && \
 apt-get install -y python python-dev python-pip python-virtualenv && \
 pip install connexion  && \
 pip install boto3 && \
 mkdir /app  && \
 rm -rf /var/lib/apt/lists/*

RUN  pip install pymongo

# Define working directory.
WORKDIR /app

# Define default command.
ENTRYPOINT python choicepoll.py

COPY . /app
RUN chmod a+x /app/choicepoll.py
