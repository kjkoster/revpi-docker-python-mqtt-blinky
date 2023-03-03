FROM python:slim-buster

RUN pip3 install paho-mqtt

ADD ./blinky.py /app/blinky.py

WORKDIR /app

CMD python3 /app/blinky.py
