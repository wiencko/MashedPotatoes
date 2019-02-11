# import libraries
import urllib2
from re import compile
from bs4 import BeautifulSoup
import text
import schedule
import time
import threading
import sys

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


def schedule_loop():
    while True:
        schedule.run_pending()
        time.sleep(30)

def new_alert():
    while True:
        print "Add New Cafeteria Alert: "
        number = raw_input('Enter your number: ')
        if (number.lower() == 'stop'):
            return
        print "Enter the name of the food: ",
        food = sys.stdin.readline()
        if (food.lower() == 'stop'):
            return
        print "What time do you want to be notified: ",
        time = sys.stdin.readline()
        if (time.lower() == 'stop'):
            return
            
        if number == "":
            continue
        if food == "":
            continue
        if time == "":
            continue
        
        #Input parsing
        food = food[0:-1]
        time = time[0:-1]
        number = "".join(number.split("-"))
        number = "".join(number.split("("))
        number = "".join(number.split(")"))
        number = "".join(number.split("/"))
        
        #Get rid of extra spaces
        number = "".join(number.split(" "))
        
        #Get rid of extra spaces except for the ones 
        #in between foods
        food = food.split(" ")
        food2 = []
        for word in food:
            word = word.lower()
            if word != "and":
                word = word.capitalize()
            if word != "":
                food2.append(word)
        food = " ".join(food2)
        
        #Input parsing
        time = " ".join(time.split(":"))
        time2 = time.lower()
        time2 = "".join(time2.split("pm"))
        addtotimehours = 0
        if time2 != time:
            time2 = time2.split(" ")
            addtotimehours = 12
            #time2[0] = str(12 + int(time2[0]))
            time2 = " ".join(time2)
        time = "".join(time2.split("am"))  
        
        #Get rid of extra spaces
        time = time.split(" ")
        time3 = []
        for nums in time:
            if nums != "":
                time3.append(nums)
        if len(time3) > 2:
            print "Bad time input"
            break
        
        if addtotimehours > 0:
            time3[0] = str(addtotimehours + int(time3[0]))
        time = ":".join(time3)
        
        #Actually Write to file
        openfile = open('textschedules.txt', 'a')
        openfile.write("%s,%s,%s\n" % (number, food, time))
        openfile.close()
        schedule.every().day.at(time).do(search_and_text, food, number)
    


schedule.every().day.at("3:00").do(pullpage, dining_website)
schedule.every().day.at("3:05").do(reschedule, schedules_list)


       
t = threading.Thread(target=schedule_loop)
t.start()

s = threading.Thread(target=new_alert)
s.start()
