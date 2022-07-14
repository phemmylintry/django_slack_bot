# syntax=docker/dockerfile:1
FROM python:3.8-slim-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]
