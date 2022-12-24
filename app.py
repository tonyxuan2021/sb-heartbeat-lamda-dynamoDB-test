import json
from flask import Flask, request
from flask_cors import CORS, cross_origin
import boto3
from decimal import Decimal


app = Flask(__name__)

dynamodb = boto3.resource(
    "dynamodb",
    region_name="us-east-1",
    endpoint_url="https://dynamodb.us-east-1.amazonaws.com",
)
table = dynamodb.Table("heartbeat")


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


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
