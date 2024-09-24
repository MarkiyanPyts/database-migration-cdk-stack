import json

def handler(event, context):
    try:
        # Extract 'users' from body parameters
        body = json.loads(event.get('body'))
        users = body.get('users')

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
