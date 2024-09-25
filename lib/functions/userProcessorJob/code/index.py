import json
import boto3
import os

sqs = boto3.client('sqs')

def handler(event, context):
    USERS_QUEUE_URL = os.getenv('USERS_QUEUE_URL', '')
    
    try:
        # Extract 'users' from body parameters
        body = json.loads(event.get('body'))
        user_data = body.get('user_data')

        # Check if 'users' is empty
        if not user_data:
            raise ValueError("No users provided")
        
        # Log the users for debugging purposes
        print("Received users: " + json.dumps(users))
        
        # Prepare a response
        response = {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": "triggered jobs for users:",
                "users": user_data
            })
        }

    except (ValueError) as e:
        # Handle any JSON parsing or missing data errors
        print(f"Error parsing event: {str(e)}")
        response = {
            "statusCode": 400,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": "Error processing the event",
                "error": str(e)
            })
        }

    return response
