FROM python:3

ENV PYTHONUNBUFFERED 1
RUN mkdir /code
COPY . /code/
WORKDIR /code
RUN pip3 install -r requirements.txt

