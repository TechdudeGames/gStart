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

def getmenunumber(minnumber,maxnumber,prompt_text = "\nInput:"):
	keeptrying = True
	attempted_input = ""
	while keeptrying:
		attempted_input = input(prompt_text)
		if attempted_input.isnumeric():
			if float(attempted_input) % 1 == 0.0:
				if (int(attempted_input) <= maxnumber) and (int(attempted_input) >= minnumber):
					keeptrying = False
				else:
					print("Invalid input, try again.")
			else:
				print("Invalid input, try again.")
		else:
			print("Invalid input, try again.")
	return int(attempted_input)

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
emails_submenu = '''
What would you like to do?
1) Add a new email
2) Remove a current email
3) Go back to the main menu
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
			mainresponse = getmenunumber(1,3)
			if mainresponse == 1:
				print("Unfinished, try again later")
			elif mainresponse == 2:
				print(emails_submenu)
				emailsubmenu_input = getmenunumber(1,3)
				if emailsubmenu_input == 1:
					addingemail = True
					print("Please send an email with the text ADDME to the email address MailWatcher uses.")
					print("Press enter when you have done so.")
					input()
					while addingemail:
						gmaildata = gmailworker.getgmailemails(service, labels=['INBOX'])
						if gmaildata == None:
							print("We had an error getting the mail, retry? (1=Yes 2=No)")
							continueaddingemail = getmenunumber(1, 2)
							if continueaddingemail == 2:
								addingemail = False
						elif gmaildata['resultSizeEstimate'] == 0:
							print("We can't find any new emails in your inbox. Try sending it again.")
							print("Press enter when you have done so.")
							input()
						else:
							worthysenders = []
							for tmpmailobj in gmaildata['messages']:
								if tmpmailobj != None:
									observed_email = gmailworker.getemaildata(service, tmpmailobj['id'])
									metadata = observed_email['payload']['headers']
									for name_data in metadata:
										if name_data['name'] == 'From':
											if observed_email['snippet'] == "ADDME":
												worthysenders.append(name_data['value'])
												gmailworker.deleteemail(service, tmpmailobj['id'])
							if worthysenders.__len__() == 0:
								print("It appears no emails have the ADDME text in them, retry? (1=Yes 2=No)")
								continueaddingemail = getmenunumber(1, 2)
								if continueaddingemail == 2:
									addingemail = False
							else:
								print("Available Emails:")
								for praisedsender in range(0, worthysenders.__len__()):
									print(praisedsender, ":", worthysenders[praisedsender])
								print("\nPick the number corresponding to the email you want to add.")
								mail_seclection = getmenunumber(0, worthysenders.__len__())
								if worthysenders[mail_seclection] in serverdata['allowed_emails']:
									print("Silly goose, that email is already on the list :)\n")
									print("Do you want to add another email? (1=Yes 2=No)")
									continueaddingemail = getmenunumber(1, 2)
									if continueaddingemail == 2:
										addingemail = False
								else:
									serverdata['allowed_emails'].append(worthysenders[mail_seclection])
									with open("data.json", 'w') as datawrite:
										json.dump(serverdata, datawrite, indent=4)
										datawrite.close()
									print("Do you want to add another email? (1=Yes 2=No)")
									continueaddingemail = getmenunumber(1, 2)
									if continueaddingemail == 2:
										addingemail = False
						
					
			else:
				print("Invalid choice.")
	
else:
	print("You seem to be missing data.json.")
	
	