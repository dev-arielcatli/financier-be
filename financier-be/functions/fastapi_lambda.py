def handler(event, context):
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "text/plain"},
        "body": "THIS IS NEW DEPLOYMENT",
    }
