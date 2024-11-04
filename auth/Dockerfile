FROM python:3.11.9

WORKDIR /src

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

COPY ./requirements.txt /src/requirements.txt

RUN pip install -r /src/requirements.txt

COPY . /src/
