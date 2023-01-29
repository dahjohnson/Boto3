import boto3
import json

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')

table = dynamodb.Table('marvel-characters')

filepath = "/home/ec2-user/environment/Boto3/dynamodb-table-mcu/mcu-dataset.json"

with open(filepath) as json_file:
    characters = json.load(json_file)
    for info in characters:
        name = info['name']
        actor = info['actor']
        realname = info['realname']
        species = info['species']
        citizenship = info['citizenship']
        dateofbirth = info['dateofbirth']
        affiliation = info['affiliation']
        appearances = info['appearances']
        image = info['image']

        print("Adding character:", name)

        table.put_item(
           Item={
               'name': name,
               'actor': actor,
               'realname': realname,
               'species': species,
               'citizenship': citizenship,
               'dateofbirth': dateofbirth,
               'affiliation': affiliation,
               'appearances': appearances,
               'image': image,
            }
        )