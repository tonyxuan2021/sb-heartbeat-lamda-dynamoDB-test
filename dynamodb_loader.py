import json
import boto3
from decimal import Decimal

# connect to AWS DynamoDB and refer to a table called heartbeat
dynamodb = boto3.resource(
    "dynamodb",
    region_name="us-east-1",
    endpoint_url="https://dynamodb.us-east-1.amazonaws.com",
)
table = dynamodb.Table("heartbeat")

# open the JSON file that has some heartbeat testing data, load this JSON file
with open("heartbeat_data.json") as json_file:
    heartbeat_data = json.load(json_file)

    # convert JSON data where it has float data structure to decimal data structure since AWS DynamoDB does not support float type, and convert it to a dictionary
    heartbeat_data_decimal = json.loads(json.dumps(heartbeat_data), parse_float=Decimal)

    # loop over the heartbeat list, and write all heartbeat data to dynamoDB heartbeat table.
    for heartbeat_record in heartbeat_data_decimal:
        user_id = heartbeat_record["user_id"]
        user_role = heartbeat_record["user_role"]
        time_stamp = heartbeat_record["time_stamp"]
        latitude = heartbeat_record["latitude"]
        longitude = heartbeat_record["longitude"]
        speed = heartbeat_record["speed"]

        response = table.put_item(
            Item={
                "user_id": user_id,
                "user_role": user_role,
                "time_stamp": time_stamp,
                "latitude": Decimal(latitude),
                "longitude": Decimal(longitude),
                "speed": int(speed),
            }
        )
