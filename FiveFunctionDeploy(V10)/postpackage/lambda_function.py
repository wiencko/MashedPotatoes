        from __future__ import print_function
        import boto3
        import time

        def lambda_handler(event, context):
            
            phone = event["From"][3:]
            admin = (phone == "15404311882")
            originaltxt = event["Body"]
            originaltxt = originaltxt.strip()
            if originaltxt == "":
                return
            txt = originaltxt.replace("+"," ")
            txt = txt.strip()
            txt = txt.split(" ")
            keyword = txt[0]
            keyword = keyword.lower()
            info = ""
            if keyword == "check":
                food = ""
                for num, word in enumerate(txt):
                    if num == 0:
                        continue
                    if num > 1:
                        food += " "
                    food += (word.lower()).capitalize()
                food = food.strip()
                publish_to_parser(food, phone)
                return
            
            
            if keyword == "clear":
                dynamo = boto3.resource('dynamodb')
                table = dynamo.Table('cafeteria')
                
                start_modifying()
                
                response = table.get_item(
                Key={"itemname": "main"}
                    )
                
                if phone in response["Item"]["phonemap"]:
                    del response["Item"]["phonemap"][phone]
                    
                table.put_item(
                    Item=response["Item"]
                    )
                   
                finish_modifying()
                 
                return return_text("Clear Successful")
                       
            if keyword == "tunnel":
                msg = ""
                for num, word in enumerate(txt):
                    if num == 0 or num == 1:
                        continue
                    if num > 2:
                        msg += " "
                    msg += word
                number = txt[1]
                number = number.replace("-","")
                number = number.replace("(","")
                number = number.replace(")","")
                number = number.replace("/","")
                if admin:
                    publish_to_sns(msg, number)
                    return return_text("Anthony, your message was sent")
                else:
                    publish_to_sns("Tunnel from: "+number+" "+msg, "15404311882" )
            
            if keyword == "add":
                food = ""
                if len(txt) == 1:
                    return return_text("Add Food Name")
                for num, word in enumerate(txt):
                    if num == 0:
                        continue
                    if num > 1:
                        food += " "
                    if word.lower() == "and" or word.lower() == "n\'":
                        food += word.lower()
                    else:
                        food += (word.lower()).capitalize()
                food = food.strip()
                
                start_modifying()
                
                dynamo = boto3.resource('dynamodb')
                table = dynamo.Table('cafeteria')
                
                response = table.get_item(
                    Key={"itemname": "main"}
                )
                if phone in response["Item"]["phonemap"]:
                    if len(response["Item"]["phonemap"][phone]) > 4:
                        info = "Currently alerting for 5 foods"
                        for food in response["Item"]["phonemap"][phone]:
                            info += "\n" + food
                    else:
                        response["Item"]["phonemap"][phone].append(food)
                        table.put_item(
                            Item=response["Item"]
                            )
                        info = "Added \"" + food + "\" Successfully!"
                else:
                    response["Item"]["phonemap"][phone] = [food]
                    table.put_item(
                        Item=response["Item"]
                        )
                    info = "Added \"" + food + "\" Successfully!"
                
                finish_modifying()
                return return_text(info)
                
            if keyword == "list":
                dynamo = boto3.resource('dynamodb')
                table = dynamo.Table('cafeteria')
                
                response = table.get_item(
                    Key={"itemname": "main"}
                )
                
                if phone in response["Item"]["phonemap"]:
                    info = "Current food alerts:"
                    for food in response["Item"]["phonemap"][phone]:
                        info += "\n" + food
                else:
                    info = "No current food alerts :("
                
                return return_text(info)
            
            if keyword == "remove":
                food = ""
                if len(txt) == 1:
                    return return_text("Remove Food Name")
                for num, word in enumerate(txt):
                    if num == 0:
                        continue
                    if num > 1:
                        food += " "
                    food += (word.lower()).capitalize()
                food = food.strip()
                
                start_modifying()
                
                dynamo = boto3.resource('dynamodb')
                table = dynamo.Table('cafeteria')
                
                response = table.get_item(
                    Key={"itemname": "main"}
                )
                if phone in response["Item"]["phonemap"]:
                    if food in response["Item"]["phonemap"][phone]:
                        response["Item"]["phonemap"][phone].remove(food)
                        table.put_item(
                            Item=response["Item"]
                            )
                        info = "Removed \"" + food + "\" Successfully!"
                    else:
                        info = food + " was not found in your alerts. Use \"list\" to check your current foods."
                
                finish_modifying()
                return return_text(info)


            info = "Commands (replace {word} with suitable word):\n"
            info += "check {food}\n"
            info += "list\n"
            info += "add {food}\n"
            info += "remove {food}\n"
            info += "clear"
            return return_text(info)

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

        def publish_to_sns(message,phone,strongout = "1"):
            sns = boto3.client('sns')
            return sns.publish(
                TopicArn='arn:aws:sns:us-west-1:664326145408:texter',
                Message=message,
                MessageStructure='string',
                Subject=phone,
                MessageAttributes={
                    'summary': {
                    'StringValue': strongout,
                        'DataType': 'String'
                        }
                    }
                )

        def start_modifying():
            dynamo = boto3.resource('dynamodb')
            table = dynamo.Table('cafeteria')
                
            response = table.get_item(
                Key={"itemname":"cstatus"}
                )
            if(response["Item"]["being_modified"]==True):
                time.sleep(2)
            else:
                table.update_item(
                Key={"itemname": "cstatus"},
                UpdateExpression="SET being_modified = :todo",
                ExpressionAttributeValues={':todo': True}
                )

        def finish_modifying():
            dynamo = boto3.resource('dynamodb')
            table = dynamo.Table('cafeteria')
            table.update_item(
                Key={"itemname": "cstatus"},
                UpdateExpression="SET being_modified = :todo",
                ExpressionAttributeValues={':todo': False}
                )
            
        def return_text(thetext):
            return'<?xml version=\"1.0\" encoding=\"UTF-8\"?>'\
                   '<Response><Message>'+ thetext +'</Message></Response>'