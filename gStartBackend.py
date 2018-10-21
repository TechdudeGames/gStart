import time

import requests
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

from gmailworker import mailfunctions


class backendfunctions:
	def __init__(self):
		self.SCOPES = 'https://mail.google.com/'
		self.store = file.Storage('token.json')
		self.creds = self.store.get()
		if not self.creds or self.creds.invalid:
			self.flow = client.flow_from_clientsecrets('credentials.json', self.SCOPES)
			self.creds = tools.run_flow(self.flow, self.store)
		self.service = build('gmail', 'v1', http=self.creds.authorize(Http()))
	
	def getmail(self, valid_senders, valid_passwords=[], verbose=True):
		'''
		:param valid_senders: A list with valid senders
		:param valid_passwords: A list with valid passwords
		:param verbose: Do you want some print statements
		:return: A dictionary with a list of the correct passwords we got, the valid emails that sent them, and the id of the message.
		'''
		checkfortext = False
		startserver = False
		unreademail = mailfunctions.getlabeledemail(self.service)
		lookatmail = False
		return_dictionary = {"passes": [], "senders": [], "ids": []}
		if unreademail == None:
			if verbose: print(time.strftime("%c"), " Unable to get the account's email.")
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
				current_email = mailfunctions.getemaildata(self.service, selectedmail['id'])
				current_sender = None
				if current_email:
					metadata = current_email['payload']['headers']
					for parse in metadata:
						if parse['name'] == 'From':
							if verbose: print(time.strftime("%c"), " Got an email from:", parse['value'])
							if parse['value'] in valid_senders:
								current_sender = mailfunctions.getemailaddr(parse['value'])
								if verbose: print(time.strftime("%c"),
								                  " Looks like someone I know, let's check the body of the email")
								checkfortext = True
				
				if checkfortext:
					msg = current_email["snippet"]  # We only need to get the first portion, so the snippet will due.
					if msg in valid_passwords:
						if verbose: print(time.strftime("%c"), " Password correct! uwu")
						return_dictionary["passes"].append(str(msg))
						return_dictionary["senders"].append(str(current_sender))
						return_dictionary["ids"].append(str(selectedmail["id"]))
					else:
						if verbose: print(time.strftime("%c"), " Password was incorrect.")
						mailfunctions.markasread(self.service, messageid=selectedmail["id"])
				else:
					mailfunctions.markasread(self.service, messageid=selectedmail["id"])
			return return_dictionary
	
	def deletevalidemails(self, idlist=[]):
		# Really we just are itterating through a list of ids and deleting the email, nothing more
		for id in idlist:
			mailfunctions.deleteemail(self.service, id)
	
	def sendmultipassemail(self, recipients=[]):
		# We litteraly just take a list of senders and send a email to them.
		msgtext = "Umm, we got multiple emails at once with different passwords, please try again later."
		for recip in recipients:
			msg = mailfunctions.createmessage("gStart MailChecker", recip, "gStart Multipassword Error", msgtext)
			mailfunctions.sendmessage(self.service, msg)
	
	def sendemailcorrectpass(self, recipients=[], servername="", port_number=0000):
		# We litteraly just take a list of senders and send a email to them.
		# We litteraly just take a list of senders and send a email to them.
		try:
			serverip = requests.get('http://ip.42.pl/raw').text
		except:
			# I am highly aware how broad this except statement is,
			serverip = "0.0.0.0"
		
		if serverip == "0.0.0.0":
			msgtext = "The server is online, but we can't figure out the ip address. All we know is the port:" + str(
				port_number)
		else:
			msgtext = "The " + servername + " has been started at " + time.strftime(
				"%c") + "\n The current server ip is: " + serverip + ":" + str(port_number)
		
		for recip in recipients:
			msg = mailfunctions.createmessage("gStart MailChecker", recip, "gStart Server Start Message", msgtext)
			mailfunctions.sendmessage(self.service, msg)
	
	def sendemailidlemode(self, recipients=[], port_number=0000):
		# We litteraly just take a list of senders and send a email to them.
		try:
			serverip = requests.get('http://ip.42.pl/raw').text
		except:
			# I am higly aware how broad this is, but there are so many exceptions when requests decided to die.
			serverip = "0.0.0.0"
		
		if serverip == "0.0.0.0":
			msgtext = "A server is online, however we are unable to see what it's ip address is"
		else:
			msgtext = "A server is already online :)" + "\n The current server ip is: " + serverip + ":" + str(
				port_number)
		
		for recip in recipients:
			msg = mailfunctions.createmessage("gStart MailChecker", recip, "gStart Server Idler Message", msgtext)
			mailfunctions.sendmessage(self.service, msg)
