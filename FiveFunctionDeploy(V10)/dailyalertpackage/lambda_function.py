import json
import boto3

def lambda_handler(event, context):
    dynamo = boto3.resource('dynamodb')
    table = dynamo.Table('cafeteria')
    
    response = table.get_item(
        Key={"itemname": "main"}
    )
    
    for number in response["Item"]["phonemap"]:
        for food in response["Item"]["phonemap"][number]:
            publish_to_parser(food, number)
    
def publish_to_parser(message,phone):
    sns = boto3.client('sns')
    return sns.publish(
        TopicArn='arn:aws:sns:us-west-1:664326145408:CafeteriaAlert',
        Message=message,
        MessageStructure='string',
        Subject=phone,
        MessageAttributes={
            'summary': {
                'StringValue': 'just a summary',
                'DataType': 'String'
            }
        }
    )