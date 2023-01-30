import boto3
import json

queue_name = 'demo-sqs-queue-luit-2023'

client = boto3.client('sqs')

queue = client.get_queue_url(
    QueueName=queue_name)

response = client.receive_message(
    QueueUrl=queue['QueueUrl'],
    MaxNumberOfMessages=10
)

print(json.dumps(response,indent=2))