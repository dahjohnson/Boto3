import boto3
import json

dynamodb = boto3.client('dynamodb')

response = dynamodb.scan(
    TableName='marvel-characters')
    
for i in response['Items']:
    print(json.dumps(i, indent=2))