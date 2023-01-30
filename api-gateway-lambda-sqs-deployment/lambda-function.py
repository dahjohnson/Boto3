import boto3
import json
from datetime import datetime

def lambda_handler(event, context):
    
    # Enter Your REGION and REGION Specific Queue URL
    queue_url = 'https://sqs.<REGION>.amazonaws.com/<ACCOUNT ID>/demo-sqs-queue-luit-2023'
    
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S %p UTC")
    
    success_message = f"Successful Connection @ {current_time}!"
    
    sqs = boto3.client('sqs')
    
    sqs.send_message(
        QueueUrl=queue_url,
        MessageBody=success_message
    )
    return {
        'statusCode': 200,
        'body': json.dumps(success_message)
    }