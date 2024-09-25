import json
import boto3
import os

sqs = boto3.client('sqs')


def handler(event, context):
    USERS_QUEUE_URL = os.getenv('USERS_QUEUE_URL', '')
    try:
        response = sqs.receive_message(
            QueueUrl=USERS_QUEUE_URL,
            AttributeNames=[
                'SentTimestamp'
            ],
            MaxNumberOfMessages=10,
            MessageAttributeNames=[
                'All'
            ],
            WaitTimeSeconds=5
        )

        message = response['Messages'][0]
        receipt_handle = message['ReceiptHandle']
        
        # Prepare a response
        response = {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": "Successfully polled users",
                "receivedUsers": response['Messages']
            })
        }

    except (ValueError) as e:
        # Handle any JSON parsing or missing data errors
        print(f"Error polling users: {str(e)}")
        response = {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": "Error polling users:",
                "error": str(e)
            })
        }

    return response
