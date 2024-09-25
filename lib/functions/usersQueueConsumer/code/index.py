import json
import boto3
import os

sqs = boto3.client('sqs')


def handler(event, context):
    USERS_QUEUE_URL = os.getenv('USERS_QUEUE_URL', '')
    try:
        # Extract 'users' from body parameters
        body = json.loads(event.get('body'))
        users = body.get('users')

        # Check if 'users' is empty
        if not users:
            raise ValueError("No users provided")
        
        # Log the users for debugging purposes
        print("Received users: " + json.dumps(users))

        users_sent = []
        # Send a message to the queue for each user
        for user_id in users:
            response = sqs.send_message(
                QueueUrl=USERS_QUEUE_URL,
                MessageBody=json.dumps({"user_id": user_id})
            )
            users_sent.append({"user_id": user_id, "sqs_message_id": response.get('MessageId')})
        
        # Prepare a response
        response = {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": "Sent users to queue",
                "users_sent": users_sent
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
                "message": "Error submitting users to queue",
                "error": str(e)
            })
        }

    return response
