import json
import boto3
from bs4 import BeautifulSoup
from re import compile
import time
import urllib2

def lambda_handler(event, context):
	food = event["Records"][0]["Sns"]["Message"]
	number = event["Records"][0]["Sns"]["Subject"]
	info = ""
	website = "https://hospitality.usc.edu/residential-dining-menus/"
	page = urllib2.urlopen(website)
	soup = BeautifulSoup(page, 'html.parser')
	today = False
	for item in soup.find_all('div', 'hsp-accordian-container'):
		meal = False 
		for cafeteria in item.contents[1].contents:
					
			if food in cafeteria.prettify():
				if today == False:
					info = info + food + " will be served today!\n"
					today = True
									
				if meal == False:
					meal = True
					mealinfo = (item.contents[0].contents[1].string).split(" ")[0]
					mealinfo += " - " + (item.contents[0].contents[1].string).split(" ")[4]  
					mealinfo += " " + ((item.contents[0].contents[1].string).split(" ")[5]).split(",")[0]
					info += mealinfo + "\n"
									
				for num, fooditem in enumerate(set(soup.find_all(text=compile(food)))):
					if num > 0:
						info += ", "
					info += fooditem
									
				info += "\n"
				cafe = (cafeteria.contents[0].string).split(" ")[0]
				if cafe == "USC":
					cafe = "The Village"
				if cafe == "Everybody's":
					cafe = "EVK"
				info = info + "@ " + cafe + "\n"
	
	if info == "":
		info = "Sorry, the USC Cafeterias are not serving " + food + " today"
	
	info = ''.join([i if ord(i) < 128 else ' ' for i in info])
	if len(info)>840:
		publish_to_sns(info[0:840], number)
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