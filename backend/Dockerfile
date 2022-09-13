FROM python:3.10-slim

CMD export PYTHONPATH="${PYTHONPATH}:/backend"

WORKDIR /backend

COPY requirements.txt .

RUN apt update && apt upgrade -y

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt --no-cache-dir

ENV PYTHONPATH "${PYTHONPATH}:/backend"
ENV PYTHONUNBUFFERED 1

COPY . ./backend

WORKDIR backend/app
