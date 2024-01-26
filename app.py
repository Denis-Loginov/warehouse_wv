import os
from flask import Flask
from sqlalchemy import create_engine
from dotenv import load_dotenv
from models import DeclarativeBase

load_dotenv()

user = os.getenv('USER')
password = os.getenv('PASSWORD')

app = Flask(__name__)
connection_string = f'mysql+pymysql://{user}:{password}@localhost/warehousedb'
engine = create_engine(connection_string)
DeclarativeBase.metadata.create_all(engine)

# Importing routes from routes.py
from routes import *

if __name__ == '__main__':
    app.run(debug=True)
