import json

def handler(event, context):
    try:
        # Extract 'users' from body parameters
        body = json.loads(event.get('body'))
        users = body.get('users')
        print("Received event: " + json.dumps(event))
        # Check if 'users' is empty
        if not users:
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
                "message": "Hello from usersQueueConsumer",
                "receivedUsers": users
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
