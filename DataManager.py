#!/usr/bin/python3
'''
The only purpose of this program is to allow the management  of valid emails in the data.json file.
'''
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import gmailworker
import os
import sys
import json
#We are going to need to get some emails, so we are going to need some gmail api magic.
SCOPES = 'https://mail.google.com/'
store = file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
	flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
	creds = tools.run_flow(flow, store)
service = build('gmail', 'v1', http=creds.authorize(Http()))

print("Email Manager\n"
      "TechdudeGames Inc.")
print("\nNote: I recommend that you have MailWatcher stopped while preforming these actions\n")

mainmenu = '''
\n
		What would you like to do?
		1) Manage Servers
		2) Manage Emails
		3) Quit
		'''
servers_submenu = '''
\n
What would you like to do?
1) Modify a preexisting server
2) Remove a preexisting server
3) Add a new server
			'''
if os.path.isfile("data.json"):
	keepongoing = True
	validfile = False
	with open('data.json', 'r') as file:
		try:
			serverdata = json.load(file)
			validfile = True
			file.close()
		except json.decoder.JSONDecodeError:
			# This only occurs if the json file is broken.
			print('Your data.json file is malformed.')
	if validfile:
		while keepongoing:
			print(mainmenu)
			mainresponse = input("Choice>")
			if mainresponse == "1":
				print(servers_submenu)
				subresponse = input("Choice>")
				if subresponse == "1":
					print("hahlol")
			else:
				print("Invalid choice.")
	
else:
	print("You seem to be missing data.json.")
	
	