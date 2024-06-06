import bson.json_util
from scrape import get_trends
from dotenv import load_dotenv
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import flask
import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

import bson

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


load_dotenv()


URI = 'mongodb+srv://{username}:{password}@cluster0.jrvk75u.mongodb.net/?retryWrites=true&w=majority&appName={appname}'.format(
    username=os.environ["MONGODB_USERNAME"],
    password=os.environ["MONGODB_USER_PASSWORD"],
    appname=os.environ["MONGODB_APPNAME"]
)


# Create a new client and connect to the server
client = MongoClient(URI, server_api=ServerApi('1'))
db = client["trends-database"]
trends_collections = db["trends"]


@app.route("/")
def root_handler():
    return "Visit <code>/trends/cache or /trends/scrape</code>"


@app.route("/trends/<type>", methods=["GET"])
def trends_handler(type):
    trends = {}

    if type == "scrape":
        # Then scrape the web
        data = get_trends()

        if not data:  # If the scraping fails then return internal server error
            return "Internal Server Error", 500

        # Store the trends into the database.
        trends_collections.insert_one(trends)

    if type == "cache" or type == "scrape":
        # If the scraping is successfull then too return the data from the database.
        data = trends_collections.find_one(sort=[("date", -1)])

        # Then retrieve from the database
        trends = {
            "IP": data["IP"],
            "date": data["date"],
            "trends": data["trends"]
        }

        return jsonify(trends)

    else:
        return "Not found", 404


if __name__ == "__main__":
    app.run(host=os.environ["HOST"], port=os.environ["PORT"])
