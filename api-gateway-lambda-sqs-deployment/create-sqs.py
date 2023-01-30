import boto3

sqs_queue_name = 'demo-sqs-queue-luit-2023'

sqs = boto3.client('sqs')

response = sqs.create_queue(QueueName=sqs_queue_name)

print("Queue Url:", response['QueueUrl'])