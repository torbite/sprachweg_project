import json

def hello_world(event, context):
    """
    Lambda handler for API Gateway test endpoint
    Returns a simple hello world message
    """
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({'message': 'Desculpa amor... eu te amo - ass liz'})
    }