import json

def handler(event, context):
    response = {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "message": "Hello from usersQueueJobsTrigger"
        })
    }
    
    return response