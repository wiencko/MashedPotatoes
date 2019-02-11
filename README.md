MashedPotatos: Cafeteria Alert App
🥔Sends a daily alert text if mashed potatoes (or any other food) are on the menu for one of the USC cafeterias.

Uses Twilio and Scheduler libraries. Schedule a daily text alerting you if and when one of the USC cafeterias
has a food that you like. 

Use info:
mashedpotatoes2.py and mashedpotatoes3.py are the main program files
A text.py is needed to run both of them. A text.sample.py file is included in the version 2 and version 3 folders.
To use, change the file name to text.py and fill in the Twilio authentication info. 

Version 2 requires a line to be written for each daily reminder. 

Version 3 uses a scheduleadder.py program to add names to a file, which is read off every morning. Each of the lines in the 
textschedules.txt file then calls a one time text to the specified number. To get rid of daily alerts, you have to manually
delete the schedule line from textschedules.txt. An option in scheduleadder.py will be added in later updates/versions.

Both versions require the mashedpotatoes2.py/mashedpotatoes3.py file to be left running for text alerts.
