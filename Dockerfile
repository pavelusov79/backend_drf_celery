FROM python:3.10

RUN mkdir /wildberries_app
WORKDIR /wildberries_app
COPY . .

RUN pip install -r requirements.txt

#EXPOSE 8000
#
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


