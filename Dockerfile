FROM python:3.10

RUN mkdir /wildberries

WORKDIR /wildberries

COPY . .

RUN pip install -r requirements.txt



