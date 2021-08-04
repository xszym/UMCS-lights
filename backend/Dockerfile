# pull official base image
FROM python:3.8.1-slim-buster

ENV MICRO_SERVICE=/usr/src/app

# set working directory
RUN mkdir -p $MICRO_SERVICE
RUN mkdir -p $MICRO_SERVICE/static

WORKDIR $MICRO_SERVICE

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
#RUN apk update \
#    && apk add postgresql-dev gcc python3-dev musl-dev

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# add app
COPY . .