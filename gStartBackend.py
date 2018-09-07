from googleapiclient.discovery import build
import googleapiclient.errors
from apiclient import errors
from httplib2 import Http
from oauth2client import file, client, tools
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
	unreademail = service.users().messages().list(userId='me', labelIds=['INBOX', "UNREAD"]).execute()
	try:
		mailtolookat = unreademail['messages']
		lookatmail = True
	except:
		print("[gStartBackend] No new mail.")
		return False
	try:
		if lookatmail:
			for selectedmail in mailtolookat:
				checkfortext = False
				current_email = service.users().messages().get(userId='me', id=selectedmail['id']).execute()
				metadata = current_email['payload']['headers']
				for parse in metadata:
					if parse['name'] == 'From':
						print("[gStartBackend] Got an email from:", parse['value'])
						for issender in valid_senders:
							if issender == parse['value']:
								print("[gStartBackend] Looks like someone I know, let's check the body of the email")
								checkfortext = True
				if checkfortext:
					msg = current_email['snippet']  # We only need to get the first portion, so the snippet will due.
					if msg == password:
						print("[gStartBackend] Password correct! Starting up")
						service.users().messages().delete(userId='me', id=current_email['id']).execute()
						startserver = True
					else:
						print("[gStartBackend] Password was incorrect.")
				else:
					service.users().messages().modify(userId='me', id=current_email['id'],
					                                  body={'removeLabelIds': ['UNREAD']}).execute()
			if startserver == True:
				return True
			else:
				return False
			return False
	except googleapiclient.errors.HttpError:
		print("A Http error has occured")
	
def markcorrectpassemail(valid_senders, password):
	checkfortext = False
	unreademail = service.users().messages().list(userId='me', labelIds=['INBOX', "UNREAD"]).execute()
	lookatmail = False
	try:
		mailtolookat = unreademail['messages']
		lookatmail = True
	except:
		print("[gStartBackend] No new mail.")
	try:
		if lookatmail:
			for selectedmail in mailtolookat:
				checkfortext = False
				current_email = service.users().messages().get(userId='me', id=selectedmail['id']).execute()
				metadata = current_email['payload']['headers']
				for parse in metadata:
					if parse['name'] == 'From':
						print("[gStartBackend] Got an email from:", parse['value'])
						for issender in valid_senders:
							if issender == parse['value']:
								print("[gStartBackend] Looks like someone I know, let's check the body of the email")
								checkfortext = True
				if checkfortext:
					msg = current_email['snippet']  # We only need to get the first portion, so the snippet will due.
					if msg == password:
						print("[gStartBackend] Password correct, deleting it")
						service.users().messages().delete(userId='me', id=current_email['id']).execute()
					else:
						print("[gStartBackend] Password was incorrect.")
	except googleapiclient.errors.HttpError:
		print("A Http error has occured")
	
