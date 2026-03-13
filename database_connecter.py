from dotenv import load_dotenv
import os
from sqlalchemy import create_engine

load_dotenv()

# DB接続
user = os.getenv('DB_USER')
password = os.getenv('DB_USER_PASSWORD')
host = os.getenv('DB_HOST')
port = os.getenv('DB_PORT')
database = os.getenv('DATABASE')

url = f'postgresql://{user}:{password}@{host}:{port}/{database}'

engine = create_engine(url, echo=True)