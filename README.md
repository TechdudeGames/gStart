### gStart
A program that looks for an email on a gmail account to start a MC server.

### Purpose
If you are like me, you sometimes are paranoid about opening a network port to the outside world just to have a private Minecraft server. This project aims to help that issue.
### General Function
MailWatcher acts like that bouncer at a bar, only a bit less violent. What it does first is look at the unread emails from an alt Gmail account. If it is from a sender it recognizes, the program then looks at the body text. If the body text matches the user defined password, the program launches a command (The one you would use to start your server). All of the email related functions are facilitated by gStartBackend.

Manager is just a simple GUI to help change the password and manage the recognized email addresses.

### Files
-Provided Files:
MailWatcher.py is the program that facilitates the polling of the emails and the launch of the command. Needs data.xml
data.xml is exactly as it sounds. It stores information on the password and recognized emails. 
Manager.py is the GUI program that works with the data.xml read by MailWatcher.py
gui/manager.ui is the UI file for Manager
gStartBackend.py is just the backend needed to poll the emails.

-Files you need to include after cloning.
In order to actually use an email account to allow MailWatcher to do it's job, you need a credentials file for that account. To do this, go to https://developers.google.com/gmail/api/quickstart/python and press Enable Google API. Name the project whatever you want and agree to the Terms of Service. It will then give you a credentials.json. Place the credentails.json in the same directory as MailWatcher.py and you are good to go.

### Requirments
Just run pip3 install --upgrade google-api-python-client oauth2client pygubu and it will install everyting you will need.

### Gettng started
