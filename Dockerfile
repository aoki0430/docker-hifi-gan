FROM python:3.8-buster as builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#FROM python:3.8-buster as builder
FROM python:3.8-buster

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
COPY . .

RUN apt update && apt install -y vim ffmpeg