import boto3
import json
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

table = dynamodb.Table('marvel-characters')

favorite_hero = 'Hulk'

print("Appearances made by my favorite Marvel character: {}".format(favorite_hero))

response = table.query(
    ProjectionExpression="#nm, realname, appearances",
    ExpressionAttributeNames={ "#nm": "name" },
    KeyConditionExpression=Key('name').eq(favorite_hero)
)

for i in response[u'Items']:
    print(json.dumps(i, indent=2))