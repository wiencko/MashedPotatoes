import json
import boto3
import time
from collections import OrderedDict


def lambda_handler(event, context):
    
    mealdict = OrderedDict()
    mealdict["0"] = "Breakfast"
    mealdict["1"] = "Brunch"
    mealdict["2"] = "Lunch"
    mealdict["3"] = "Dinner"
    cafedict = OrderedDict()
    cafedict["0"] = "USC Village"
    cafedict["1"] = "Parkside" 
    cafedict["2"] = "EVK"
    
    fooddict = OrderedDict()
    for key, value in mealdict.iteritems():
        fooddict[value] = OrderedDict()
        for key2, value2 in cafedict.iteritems():
            fooddict[value][value2] = OrderedDict()
        
    food = event["Records"][0]["Sns"]["Message"]
    number = event["Records"][0]["Sns"]["Subject"]
    
    dynamo = boto3.resource('dynamodb')
    table = dynamo.Table('cafeteria')
    
    response = table.get_item(
        Key={"itemname": "foodlist"}
        )
    
    response = response["Item"]
    
    day = response["day"]
    
    matches = [line for line in response["foods"] if food.lower() in line.lower()]
    
    for match in matches:
        fooddict[mealdict[match[0]]][cafedict[match[1]]][match[3:]] = 1
    
    info = ""
    today = False
    for key in fooddict:
        meal = False
        for key2 in fooddict[key]:
            foodincafe = False
            
            for num, item in enumerate(fooddict[key][key2]):
            
                if today == False:
                    today = True
                    info = info + food + " will be served today!\n"
                
                if meal == False:
                    meal = True
                    info += key + " - " + day + "\n"
                    
                foodincafe = True
                if num > 0: info += ", "
                info += item
            
            if foodincafe:
                info += "\n@ " + key2 + "\n"
        
    if info == "":
        info = "Sorry, the USC Cafeterias are not serving " + food + " today"
    
    info = ''.join([i if ord(i) < 128 else ' ' for i in info])
    if len(info)>560:
        publish_to_sns(info[0:560], number)
    else:
        publish_to_sns(info, number)

def publish_to_sns(message,phone):
    sns = boto3.client('sns')
    return sns.publish(
        TopicArn='arn:aws:sns:us-west-1:664326145408:texter',
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
