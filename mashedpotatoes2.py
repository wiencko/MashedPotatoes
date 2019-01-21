# import libraries
import urllib2
import pymsgbox
from re import compile
from bs4 import BeautifulSoup
import text
import schedule
import time

food = "Mashed Potatoes"
my_number = "1234567890"


website = "https://hospitality.usc.edu/residential-dining-menus/"


def scrape_and_text(food, to_number):
    if food == "":
        return
    page = urllib2.urlopen(website)

    soup = BeautifulSoup(page, 'html.parser')

    info = ""
    today = False
    for item in soup.find_all('div', 'hsp-accordian-container'):
        meal = False 
        #print item.contents[0].contents[1].string
        for cafeteria in item.contents[1].contents:
            #print cafeteria.contents[0].string
            if food in cafeteria.prettify():
                if today == False:
                    today = True
                    info = info + food + " are being served today!\n"
    #                print food, "are being served today!"
                if meal == False:
                    meal = True
                    info += item.contents[0].contents[1].string + "\n"
    #                print item.contents[0].contents[1].string
                for num, fooditem in enumerate(set(soup.find_all(text=compile(food)))):
                    if num > 0:
                        info += " and "
    #                    print "and",
                    info += fooditem
    #                print fooditem,
                info += "\n"
    #            print
    #            if meal == False:
    #                meal = True
    #                info += item.contents[0].contents[1].string + "\n"
    #                print item.contents[0].contents[1].string
                info = info + "@ " + cafeteria.contents[0].string + "\n"
    #            print "@", cafeteria.contents[0].string
        
    if info != "":
        text.texter(info, to_number)
    #if food in soup.prettify():
    #    pymsgbox.alert("The cafeteria has " + food + "!!")


schedule.every().day.at("10:00").do(scrape_and_text, "Fries", my_number)
schedule.every().day.at("7:30").do(scrape_and_text, "Mashed Potatoes", my_number)

while True:
    schedule.run_pending()
    time.sleep(1)