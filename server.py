from scrape import get_trends
from dotenv import load_dotenv
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import flask
import datetime


load_dotenv()


URI = 'mongodb+srv://{username}:{password}@cluster0.jrvk75u.mongodb.net/?retryWrites=true&w=majority&appName={appname}'.format(
    username=os.environ["MONGODB_USERNAME"],
    password=os.environ["MONGODB_USER_PASSWORD"],
    appname=os.environ["MONGODB_APPNAME"]
)

# Create a new client and connect to the server
client = MongoClient(URI, server_api=ServerApi('1'))
db = client["trends-database"]
