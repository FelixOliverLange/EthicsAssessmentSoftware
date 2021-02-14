FROM debian:buster-slim
RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN pip3 install djangorestframework django-cors-headers pymysql
WORKDIR /code
COPY requirements.txt /code/
COPY code/ /code/
RUN pip3 install -r requirements.txt

