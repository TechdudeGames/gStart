from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import gmailworker
import time
SCOPES = 'https://mail.google.com/'
store = file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
	flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
	creds = tools.run_flow(flow, store)
service = build('gmail', 'v1', http=creds.authorize(Http()))


def checkmail(valid_senders, password):
	checkfortext = False
	startserver = False
	unreademail = gmailworker.getmail(service)
	lookatmail = False
	if unreademail == None:
		print(time.strftime("%c"), " Unable to get the accounts email.")
		return False
	elif unreademail['resultSizeEstimate'] == 0:
		print(time.strftime("%c"), " No new mail to look at.")
		return False
	else:
		mailtolookat = unreademail['messages']
		lookatmail = True
	if lookatmail:
		for selectedmail in mailtolookat:
			checkfortext = False
			current_email = gmailworker.getemail(service, selectedmail['id'])
			if current_email != None:
				metadata = current_email['payload']['headers']
				for parse in metadata:
					if parse['name'] == 'From':
						print(time.strftime("%c"), " Got an email from:", parse['value'])
						for issender in valid_senders:
							if issender == parse['value']:
								print(time.strftime("%c"),
								      " Looks like someone I know, let's check the body of the email")
								checkfortext = True
								break
				if checkfortext:
					msg = current_email['snippet']  # We only need to get the first portion, so the snippet will due.
					if msg == password:
						print(time.strftime("%c"), " Password correct! Starting up")
						gmailworker.deleteemail(service, selectedmail['id'])
						startserver = True
					else:
						print(time.strftime("%c"), " Password was incorrect.")
						gmailworker.markasread(service, selectedmail['id'])
				else:
					gmailworker.markasread(service, selectedmail['id'])
		if startserver == True:
			return True
		else:
			return False
		return False


def deletecorrectpassemail(valid_senders, password):
	checkfortext = False
	startserver = False
	unreademail = gmailworker.getmail(service)
	lookatmail = False
	if unreademail == None:
		print(time.strftime("%c"), " Unable to get the accounts email.")
	elif unreademail['resultSizeEstimate'] == 0:
		print(time.strftime("%c"), " No new mail to look at.")
	else:
		mailtolookat = unreademail['messages']
		lookatmail = True
	if lookatmail:
		for selectedmail in mailtolookat:
			checkfortext = False
			current_email = gmailworker.getemail(service, selectedmail['id'])
			if current_email != None:
				metadata = current_email['payload']['headers']
				for parse in metadata:
					if parse['name'] == 'From':
						print(time.strftime("%c"), " Got an email from:", parse['value'])
						for issender in valid_senders:
							if issender == parse['value']:
								print(time.strftime("%c"),
								      " Looks like someone I know, let's check the body of the email")
								checkfortext = True
								break
				if checkfortext:
					msg = current_email['snippet']  # We only need to get the first portion, so the snippet will due.
					if msg == password:
						print(time.strftime("%c"), " Password correct, removing email")
						gmailworker.deleteemail(service, selectedmail['id'])
					else:
						gmailworker.markasread(service, selectedmail['id'])
				else:
					gmailworker.markasread(service, selectedmail['id'])