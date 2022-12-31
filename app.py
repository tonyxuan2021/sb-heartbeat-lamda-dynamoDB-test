import json
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal
import logging

# logger is used to debug Lambda functions at AWS CloudWatch
logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)

# set max lookback heartbeat record to 10
MAX_LOOKBACK = 10

# retrive the heartbeat table from DynamoDB
dynamodb = boto3.resource(
    "dynamodb",
    region_name="us-east-1",
    endpoint_url="https://dynamodb.us-east-1.amazonaws.com",
)
table = dynamodb.Table("heartbeat")

# returns all heartbeat data in dynamodb
@app.route("/heartbeat")
@cross_origin()
def get_all_heartbeat():

    response = table.scan()["Items"]
    logger.info("All heartbeat data returned")
    return jsonify(response)


# create an endpoint that has the business logic to accept data from FE and write to heartbeat table
@app.route("/heartbeat", methods=["POST"])
@cross_origin()
def heartbeatpost():
    data = json.loads(request.get_data())
    user_id = data["userId"]
    user_role = data["userRole"]
    time_stamp = data["timestamp"]
    latitude = data["latitude"]
    longitude = data["longitude"]
    speed = data["speed"]

    if (
        not user_id
        or not user_role
        or not time_stamp
        or not latitude
        or not longitude
        or not speed
    ):
        return "Unable to write to server due to missing attribute(s)", 400

    post_heartbeat(user_id, user_role, time_stamp, latitude, longitude, speed)
    return "Heartbeat data added successfully", 200


# GET heartbeats by user_id
@app.route("/heartbeat/<user_id>", methods=["GET"])
@cross_origin()
def get_heartbeats_by_user_id(user_id):
    # convert user_id to a integer, otherwise the post request will be return a 500 error message
    user_id = int(user_id)

    # make a query from heartbeat table, and return all the heartbeat record that match with the queried user_id
    user_exists = table.query(KeyConditionExpression=Key("user_id").eq(user_id))

    # create a lookback variable to retrive the lookback value after the question mark from the endpoint address
    lookback = request.args.get("lookback")

    # check if user_id exists
    if not user_exists:
        return "No heartbeats found for this user_id", 400

    # check if lookback parameter is valid type and within range
    if lookback:
        try:
            lookback = int(lookback)
        except ValueError:
            return "Invalid type, lookback must be an integer", 400

        if lookback > MAX_LOOKBACK:
            return f"Maximum lookback limit exceeded (max: {MAX_LOOKBACK})", 400

        # get multiple heartbeats
        data = get_latest_heartbeats(user_id, lookback)

    else:
        # get single heartbeat
        data = get_latest_heartbeats(user_id)

    # return requested heartbeat data to user
    return jsonify(data["Items"])


def get_latest_heartbeats(user_id, lookback=1):
    user_id = int(user_id)
    return table.query(
        # make a query from heartbeat table, and return all the heartbeat record that match with the queried user_id
        KeyConditionExpression=Key("user_id").eq(user_id),
        # sort time_stamp(Sort key) by decending order
        ScanIndexForward=False,
        # set the number of returning data limit
        Limit=lookback,
    )


def post_heartbeat(id, role, timestamp, lat, long, speed):

    table.put_item(
        Item={
            "user_id": id,
            "user_role": role,
            "time_stamp": timestamp,
            "latitude": Decimal(str(lat)),
            "longitude": Decimal(str(long)),
            "speed": speed,
        }
    )
