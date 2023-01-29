import boto3

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('marvel-characters')

table.delete()

print("Table status:", table.table_status)