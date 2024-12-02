FROM python:3.10

RUN mkdir /wildberries

WORKDIR /wildberries

RUN pip install -r requirements.txt

COPY . .





