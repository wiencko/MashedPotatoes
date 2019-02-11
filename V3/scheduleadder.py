#!/usr/bin/python

import sys

while True:
    print "Add New Cafeteria Alert: "
    number = raw_input('Enter your number: ')
    print "Enter the name of the food: ",
    food = sys.stdin.readline()
    print "What time do you want to be notified: ",
    time = sys.stdin.readline()
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
    
