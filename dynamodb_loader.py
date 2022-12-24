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

with open("heartbeat_data.json") as json_file:
    heartbeat_data = json.load(json_file)
    heartbeat_data_decimal = json.loads(json.dumps(heartbeat_data), parse_float=Decimal)

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
                "latitude": latitude,
                "longitude": longitude,
                "speed": speed,
            }
        )
        print("Put item succeeded")
        print(json.dumps(response, indent=4))


# heartbeat_data_decimal = json.loads(json.dumps(heartbeat_data), parse_float=Decimal)

# find the JSON file in folder and read it

# convert JSON data where it has float -> decimal since AWS DynamoDB does not support float type, and convert JSON file to disctionary

# loop over the converted heartbeat data, and assign a name to each property in the dictionary

# write all heartbeat data to DynamoDB
