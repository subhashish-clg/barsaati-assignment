import bson.json_util
from scrape import get_trends
from dotenv import load_dotenv
import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import flask
import datetime
from flask import Flask, request, jsonify
import bson

app = Flask(__name__)


load_dotenv()


URI = 'mongodb+srv://{username}:{password}@cluster0.jrvk75u.mongodb.net/?retryWrites=true&w=majority&appName={appname}'.format(
    username=os.environ["MONGODB_USERNAME"],
    password=os.environ["MONGODB_USER_PASSWORD"],
    appname=os.environ["MONGODB_APPNAME"]
)


def dto(db_record):
    return {
        "date": db_record["date"],
        "IP": db_record["IP"] if "IP" in db_record else None,
        "trends": db_record["trends"]
    }


# Create a new client and connect to the server
client = MongoClient(URI, server_api=ServerApi('1'))
db = client["trends-database"]
trends_collections = db["trends"]


@app.route("/trends")
def hello_world():
    fallback = request.args.get("fallback")

    if fallback == "latest":
        # Then scrape the web
        data = get_trends()

        if not data:
            return "Internal Server Error", 500

        IP, trends = data

        trends_collections.insert_one({
            "IP": IP, "date": datetime.datetime.now(tz=datetime.UTC), "trends": trends
        })

        return jsonify({
            "IP": IP,
            "trends": trends
        })

    else:
        # Then retrieve from the database
        trends = trends_collections.find_one(sort=[("date", -1)])

        return jsonify({
            "IP": trends["IP"],
            "trends": trends["trends"]
        })


if __name__ == "__main__":
    app.run(host=os.environ["HOST"], port=os.environ["PORT"])
