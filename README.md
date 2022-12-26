# Serverless Framework Python Flask API on AWS

This template demonstrates how to invoke the Python Flask API service running on AWS Lambda using the traditional Serverless Framework.

## Usage

you can call the created application via Postman:

POST "/heartbeat" - write heartbeat data to HeartbeatDriver table

```bash
https://n3qpywkfle.execute-api.us-east-1.amazonaws.com/dev/heartbeat
```

Sample body:

```
{
    "userId": 1,
    "userRole": "driver",
    "timestamp": 1669980289,
    "latitude": 18.0016,
    "longitude": -78.8926,
    "speed": 50
}
```

Which should result in the following response:

```
"Heartbeat data added successfully"
```

GET "/heartbeat/<user_id>/?lookback=<#>" - read heartbeats by user_id, with a optional lookback value

Which should result in the following response(without a lookback value):

```
[
    {
        "latitude": "18.0266",
        "longitude": "-76.7721",
        "speed": "40",
        "time_stamp": "1669980529",
        "user_id": "1",
        "user_role": "driver"
    }
]
```
