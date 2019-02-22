from __future__ import print_function
import boto3
import time

def lambda_handler(event, context):
    
    txt = event["Body"]
    txt = txt.strip()
    if txt == "":
        return
    txt = txt.replace("+"," ")
    txt = txt.strip()
    txt = txt.split(" ")
    keyword = txt[0]
    keyword = keyword.lower()
    if keyword == "check":
        food = ""
        for num, word in enumerate(txt):
            if num == 0:
                continue
            if num > 1:
                food += " "
            food += word.capitalize()
        food = food.strip()
        publish_to_sns(food, event["From"][3:])
        return
    
    
    if keyword == "clear":
        dynamo = boto3.resource('dynamodb')
        table = dynamo.Table('cafeteria')
        response = table.get_item(
            Key={"itemname": "cstatus"}
            )
        updateitem = response["Item"]
        if(updateitem["being_modified"] == True):
            time.sleep(5)
        else:
            table.update_item(
                Key={"itemname": "cstatus"},
                UpdateExpression="SET being_modified = :todo",
                ExpressionAttributeValues={':todo': True}
                )
        response = table.get_item(
        Key={"itemname": "main"}
            )
        curritem = response["Item"]
        
        if event["From"] in curritem["messages"]:
            del curritem["messages"][event["From"]]
            
        table.put_item(
            Item=curritem
            )
           
        table.update_item(
            Key={"itemname": "cstatus"},
            UpdateExpression="SET being_modified = :todo",
            ExpressionAttributeValues={':todo': False}
        )
        
         
        return '<?xml version=\"1.0\" encoding=\"UTF-8\"?>'\
               '<Response><Message>'+ "Clear successful" +'</Message></Response>'
               
    #if keyword == "test":
        
        
        
        
        
    
    dynamo = boto3.resource('dynamodb')
    table = dynamo.Table('cafeteria')
    
    response = table.get_item(
        Key={"itemname": "cstatus"}
        )
    
    updateitem = response["Item"]
    
    print()  
    print("mystuff")
    print(response)
    print()
    print(updateitem)
    if(updateitem["being_modified"] == True):
        time.sleep(5)
        # response = table.get_item(
        # Key={"itemname": "cstatus"}
        # )
        # updateitem = response["Item"]
    else:
        print("wasfalse")
        table.update_item(
            Key={"itemname": "cstatus"},
            UpdateExpression="SET being_modified = :todo",
            ExpressionAttributeValues={':todo': True}
            )
    
    phone = event["From"]
    msg = event["Body"]
    response = table.get_item(
        Key={"itemname": "main"}
        )
    curritem = response["Item"]
    
    msg = msg.replace("+"," ")
    msg = msg.strip()
    msg = msg.split(" ")
    parsedin = ""
    for word in msg:
       if word != " " and word != "":
           parsedin += (word.lower()).capitalize() + " "
    parsedin = parsedin.strip()
       
        
    if phone in curritem["messages"]:
        curritem["messages"][phone].append(parsedin)
    else:
        curritem["messages"][phone] = [parsedin]
    
    table.put_item(
        Item=curritem
        )

    table.update_item(
        Key={"itemname": "cstatus"},
        UpdateExpression="SET being_modified = :todo",
        ExpressionAttributeValues={':todo': False}
        )
    
    
    return '<?xml version=\"1.0\" encoding=\"UTF-8\"?>'\
           '<Response><Message>'+ "Message stored" +'</Message></Response>'


def publish_to_sns(message,phone):
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