from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import requests
import gmailworker
import time
SCOPES = 'https://mail.google.com/'
store = file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
	flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
	creds = tools.run_flow(flow, store)
service = build('gmail', 'v1', http=creds.authorize(Http()))

def getmails(valid_senders, valid_passwords=[], verbose=True):
	'''
	:param valid_senders: A list with valid senders
	:param valid_passwords: A list with valid passwords
	:param verbose: Do you want soem print statements
	:return: A dictionary with a list of the correct passwords we got, the valid emails that sent them, and the id of the message.
	'''
	checkfortext = False
	startserver = False
	unreademail = gmailworker.getgmailemails(service)
	lookatmail = False
	return_dictionary = {"passes": [], "senders" : [], "ids": []}
	if unreademail == None:
		if verbose: print(time.strftime("%c"), " Unable to get the accounts email.")
		return return_dictionary
	elif unreademail['resultSizeEstimate'] == 0:
		if verbose: print(time.strftime("%c"), " No new mail to look at.")
		return return_dictionary
	else:
		mailtolookat = unreademail['messages']
		lookatmail = True
	if lookatmail:
		for selectedmail in mailtolookat:
			checkfortext = False
			current_email = gmailworker.getemaildata(service, selectedmail['id'])
			current_sender = None
			if current_email != None:
				metadata = current_email['payload']['headers']
				for parse in metadata:
					if parse['name'] == 'From':
						if verbose:print(time.strftime("%c"), " Got an email from:", parse['value'])
						for issender in valid_senders:
							if issender == parse['value']:
								current_sender = gmailworker.getemailaddr(parse['value'])
								if verbose:print(time.strftime("%c"),
								      " Looks like someone I know, let's check the body of the email")
								checkfortext = True
								break
			if checkfortext:
				msg = current_email["snippet"]  # We only need to get the first portion, so the snippet will due.
				if msg in valid_passwords:
					if verbose: print(time.strftime("%c"), " Password correct! uwu")
					return_dictionary["passes"].append(str(msg))
					return_dictionary["senders"].append(str(current_sender))
					return_dictionary["ids"].append(str(selectedmail["id"]))
				else:
					if verbose: print(time.strftime("%c"), " Password was incorrect.")
					gmailworker.markasread(service, messageid=selectedmail["id"])
			else:
				if verbose: print(time.strftime("%c"), " Password was incorrect.")
				gmailworker.markasread(service, messageid=selectedmail["id"])
		return return_dictionary
	
def deletevalidemails(idlist = []):
	#Really we just are itterating through a list of ids and deleting the email, nothing more
	for id in idlist:
		gmailworker.deleteemail(service,id)
		
def sendmultipassemail(recipients= []):
	#We litteraly just take a list of senders and send a email to them.
	for recip  in recipients:
		msgtext = "Umm, we got multiple emails at once with different passwords, please try again later."
		msg = gmailworker.createmessage("gStart MailChecker", recip,"gStart Multipassword Error", msgtext)
		gmailworker.sendmessage(service,msg)

def sendemailcorrectpass(recipients = [], servername = "",port_number = 0000):
	# We litteraly just take a list of senders and send a email to them.
	for recip in recipients:
		msgtext ="The " + servername + " has been started at" + time.strftime("%c") + "\n The current server ip is: " + str(
			requests.get('http://ip.42.pl/raw').text) + ":" + str(port_number)
		msg = gmailworker.createmessage("gStart MailChecker", recip, "gStart Server Start Message", msgtext)
		gmailworker.sendmessage(service,msg)
		
def sendemailidlemode(recipients = [], port_number = 0000):
	# We litteraly just take a list of senders and send a email to them.
	for recip in recipients:
		msgtext = "A server is already online :)" + "\n The current server ip is: " + str(
			requests.get('http://ip.42.pl/raw').text) + ":" + str(port_number)
		msg = gmailworker.createmessage("gStart MailChecker", recip, "gStart Server Idler Message", msgtext)
		gmailworker.sendmessage(service,msg)