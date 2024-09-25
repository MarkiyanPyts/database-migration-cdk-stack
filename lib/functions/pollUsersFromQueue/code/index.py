import json
import boto3
import os

sqs = boto3.client('sqs')
eventsClient = boto3.client('events')

def handler(event, context):
    USERS_QUEUE_URL = os.getenv('USERS_QUEUE_URL', '')
    EVENT_BUS_NAME = os.getenv('EVENT_BUS_NAME', '')
    EVENT_SOURCE = os.getenv('EVENT_SOURCE', '')

    try:
        polled_messages = 0
        no_more_messages = False
        array_of_started_jobs = []
        # Poll for messages
        while polled_messages < 50 and not no_more_messages:
            response = sqs.receive_message(
                QueueUrl=USERS_QUEUE_URL,
                MaxNumberOfMessages=1,
            )
            print(f"Received users: {response}")
            if response['Messages'] and len(response['Messages']) > 0:
                message = response['Messages'][0]
                
                # receipt_handle = message['ReceiptHandle']

                send_event_response = eventsClient.put_events(
                    Entries=[
                        {
                            'Source': EVENT_SOURCE,
                            'Detail': json.dumps(message),
                            'EventBusName': EVENT_BUS_NAME,
                        },
                    ],
                )
                print('send_event_response:' + send_event_response)
                array_of_started_jobs.append(message)
                polled_messages += 1
            else:
                no_more_messages = True
        
        # Prepare a response
        response = {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps({
                "message": "Successfully started jobs for following messages:",
                "receivedUsers": array_of_started_jobs
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
