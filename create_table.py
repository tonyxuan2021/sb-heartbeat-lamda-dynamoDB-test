from flask import Flask
import boto3


dynamodb = boto3.resource(
    "dynamodb",
    region_name="us-east-1",
    endpoint_url="https://dynamodb.us-east-1.amazonaws.com",
)

table = dynamodb.create_table(
    TableName="heartbeat",
    KeySchema=[{"AttributeName": "heartbeat_id", "KeyType": "HASH"}],  # Partition key
    AttributeDefinitions=[
        {"AttributeName": "user_id", "AttributeType": "N"},
    ],
    ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
)
