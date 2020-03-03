FROM python:3.7-slim

RUN apt-get update && \
    apt-get install -y git

RUN mkdir /server
WORKDIR /server

COPY ./requirements.txt /server/
RUN pip install -r requirements.txt

COPY ./server /server
