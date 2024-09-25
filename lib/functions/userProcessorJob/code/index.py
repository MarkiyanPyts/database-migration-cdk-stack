import json
import boto3
import os

sqs = boto3.client('sqs')

def handler(event, context):
    USERS_QUEUE_URL = os.getenv('USERS_QUEUE_URL', '')
    
    try:
        print('event:')
        print(event)
        print('context:')
        print(context)
        
        # Prepare a response
        response = {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": "triggered jobs for users:",
            })
        }

    except (ValueError) as e:
        # Handle any JSON parsing or missing data errors
        print(f"Error parsing event: {str(e)}")
        response = {
            "statusCode": 500,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": "Error processing user",
                "error": str(e)
            })
        }

    return response
