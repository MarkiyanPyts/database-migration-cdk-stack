import json
import boto3
import os

sqs = boto3.client('sqs')

def handler(event, context):
    USERS_QUEUE_URL = os.getenv('USERS_QUEUE_URL', '')
    
    try:
        event_details = event['detail']
        

        sqs_receipt_handle = event_details['ReceiptHandle']
        sqs_message_id = event_details['MessageId']
        user_data = event_details['Body']
        print('sqs_receipt_handle:')
        print(sqs_receipt_handle)
        print('sqs_message_id:')
        print(sqs_message_id)
        print('user_id:')
        print(user_data['user_id'])

        ## do migration for this user...if transaction was success delete SQS message
        sqs.delete_message(
            QueueUrl=USERS_QUEUE_URL,
            ReceiptHandle=sqs_receipt_handle
        )
        
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
