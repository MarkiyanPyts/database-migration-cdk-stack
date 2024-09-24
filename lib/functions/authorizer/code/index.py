def handler(event, context):
    # Extract the token from the Authorization header
    token = event.get('headers', {}).get('Authorization', None)
    print("token = ", token)
    effect = "Deny"

    # Check if the token matches
    if token == "Bearer innovation_1":
        effect = "Allow"
    else:
        effect = "Deny"

    # Create the IAM policy for the API Gateway
    policy = {
        "principalId": "user",
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": effect,
                    "Resource": event['methodArn']
                }
            ]
        }
    }

    return policy
