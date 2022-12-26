import json
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import boto3
from boto3.dynamodb.conditions import Key
from decimal import Decimal
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)
app = Flask(__name__)

MAX_LOOKBACK = 10

dynamodb = boto3.resource(
    "dynamodb",
    region_name="us-east-1",
    endpoint_url="https://dynamodb.us-east-1.amazonaws.com",
)
table = dynamodb.Table("heartbeat")


@app.route("/heartbeat")
@cross_origin()
def get_all_heartbeat():
    """
    returns all citizen items present in dynamodb
    """
    response = table.scan()["Items"]
    logger.info("All heartbeat data returned")
    return jsonify(response)


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

    else:
        table.put_item(
            Item={
                "user_id": user_id,
                "user_role": user_role,
                "time_stamp": time_stamp,
                "latitude": Decimal(str(latitude)),
                "longitude": Decimal(str(longitude)),
                "speed": speed,
            }
        )
        return "Heartbeat data added successfully", 200


# GET heartbeats by user_id
@app.route("/heartbeat/<user_id>", methods=["GET"])
@cross_origin()
def get_heartbeats_by_user_id(user_id):
    # user_exists = Heartbeat.query.filter_by(user_id=user_id).first()
    user_id = int(user_id)

    user_exists = table.query(KeyConditionExpression=Key("user_id").eq(user_id))

    lookback = request.args.get("lookback")

    # check if user_id exists
    if not user_exists:
        return "No heartbeats found for this user_id", 400

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

    return jsonify(data["Items"])


# check if lookback parameter is valid type and within range


def get_latest_heartbeats(user_id, lookback=1):
    user_id = int(user_id)
    return table.query(
        KeyConditionExpression=Key("user_id").eq(user_id),
        ScanIndexForward=False,
        Limit=lookback,
    )
