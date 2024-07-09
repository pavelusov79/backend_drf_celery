from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASSWORD')
DB_NAME = os.environ.get('DB_NAME')
SECRET_API_KEY = os.environ.get('SECRET_API_KEY')

RMQ_USER = os.environ.get('RMQ_USER')
RMQ_PASS = os.environ.get('RMQ_PASS')
RMQ_HOST = os.environ.get('RMQ_HOST')
RMQ_PORT = os.environ.get('RMQ_PORT')
