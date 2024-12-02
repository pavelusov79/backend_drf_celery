FROM joyzoursky/python-chromedriver:3.9

ENV DISPLAY=:99

RUN mkdir /wildberries

COPY requirements.txt /wildberries

WORKDIR /wildberries

RUN pip install -r requirements.txt

COPY . .





