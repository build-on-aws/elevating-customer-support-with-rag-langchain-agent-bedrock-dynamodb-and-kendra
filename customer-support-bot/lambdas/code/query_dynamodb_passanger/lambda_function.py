#################################################
## This function is to query a dynamoDB table ###
#################################################

import json
from boto3.dynamodb.conditions import Key
import boto3
import botocore.exceptions
import os
import re

dynamodb_resource=boto3.resource('dynamodb')

table_name = os.environ.get('TABLE_PASSANGER')
key_name = os.environ.get('ENV_KEY_NAME')

table = dynamodb_resource.Table(table_name)

def db_query(key,table,keyvalue):
    response = table.query(
        KeyConditionExpression=Key(key).eq(keyvalue)
    )
    print(response)
    return response['Items'][0]


def lambda_handler(event, context):
    print(event)
    '''Handle Lambda event from AWS'''
    # Setup alarm for remaining runtime minus a second
    # signal.alarm((context.get_remaining_time_in_millis() / 1000) - 1)
    try:
        print('REQUEST RECEIVED:', event)
        print('REQUEST CONTEXT:', context)

        query = event['body']
        print(query)
        s = re.sub(r'[^a-zA-Z0-9]', '', query)
        tabla_response = db_query(key_name,table,str(s))
        print(tabla_response)

        return({"body":tabla_response})
    
    
    except Exception as error: 
        print('FAILED!', error)
        return({"body":"Cuek! no in Data Base"})

