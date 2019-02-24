import json
import boto3
from bs4 import BeautifulSoup
import urllib2
import re

def lambda_handler(event, context):
    foods = []
    website = "https://hospitality.usc.edu/residential-dining-menus/"
    print website
    page = urllib2.urlopen(website)
    soup = BeautifulSoup(page, 'html.parser')
    for mnum, item in enumerate(soup.find_all('div', 'hsp-accordian-container')):
        for cnum, cafeteria in enumerate(item.contents[1].contents):
            for item in cafeteria.find_all('ul', 'menu-item-list'):
                for section in item.contents:
                    food = re.sub(r'\([^()]*\)', '',section.contents[0].string)
                    food = ''.join([i if ord(i) < 128 else '' for i in food])
                    food = food.replace('"','')
                    food = food.replace("'",'')
                    foods.append(str(mnum)+str(cnum)+" "+food)
                    
    day = (" ".join(soup.find("h2", "fw-accordion-title ui-state-active").contents[1].string.split(" ")[4:6]))[:-1]
    item = {"itemname": "foodlist", "foods": foods, "day": day}
    dynamo = boto3.resource('dynamodb')
    table = dynamo.Table('cafeteria')
    table.put_item(
        Item=item
        )
    return "Successful"
