# import libraries
import urllib2
from re import compile
from bs4 import BeautifulSoup
import text
import schedule
import time


dining_website = "https://hospitality.usc.edu/residential-dining-menus/"

schedules_list = 'textschedules.txt'

def pullpage(website):
    
    global page 
    page = urllib2.urlopen(website)

    global soup 
    soup = BeautifulSoup(page, 'html.parser')

def search_and_text(food, to_number):
    if food == "":
        return schedule.CancelJob
        
    info = ""
    today = False
    for item in soup.find_all('div', 'hsp-accordian-container'):
        meal = False 
        for cafeteria in item.contents[1].contents:
            
            if food in cafeteria.prettify():
                if today == False:
                    today = True
                    info = info + food + " will be served today!\n"
                    
                if meal == False:
                    meal = True
                    info += item.contents[0].contents[1].string + "\n"

                for num, fooditem in enumerate(set(soup.find_all(text=compile(food)))):
                    if num > 0:
                        info += " and "
                    info += fooditem
                    
                info += "\n"
                info = info + "@ " + cafeteria.contents[0].string + "\n"
 
    if info != "":
        text.texter(info, to_number)
    return schedule.CancelJob

def reschedule(pullfile):
    openfile = open(pullfile, 'r')
    for line in openfile:
        line_list = (line.strip()).split(",")
        #schedule.every().day.at("7:30").do(search_and_text, "Mashed Potatoes", my_number)
        schedule.every().day.at(line_list[2]).do(search_and_text, line_list[1], line_list[0])
        
    openfile.close()


schedule.every().day.at("3:00").do(pullpage, dining_website)
schedule.every().day.at("3:05").do(reschedule, schedules_list)

while True:
    schedule.run_pending()
    time.sleep(30)

