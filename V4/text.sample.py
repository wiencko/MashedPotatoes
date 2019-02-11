#!/usr/bin/python

# text.py - Defines the texter() function that texts a message

# Fill in your own info
accountSID = 
authToken = 
twilioNumber = '+11234567890'

from twilio.rest import Client

def texter(message, number):
    twilioCli = Client(accountSID, authToken)
    twilioCli.messages.create(body=message, from_=twilioNumber, to=number)