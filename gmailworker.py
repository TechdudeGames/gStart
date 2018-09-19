import googleapiclient.errors
import time
import mimetypes
from email.mime.text import MIMEText
import base64
def getmail(service, labels=["INBOX", "UNREAD"]):
	'''
	:param service: The gmail service variable used to access the gmail account
	:param lables: The labels I am looking for when getting the mail
	:return: a dict of emails with their id's and threads. Will return None if no mail.
	This function only get's a list of emails with certain labels
	'''
	#This will attempt to get the emails 3 times
	mail = None
	for i in range(0,3):
		try:
			mail = service.users().messages().list(userId='me', labelIds=labels).execute()
			break
		except googleapiclient.errors.HttpError:
			time.sleep(2)
	return mail

def getemail(service,messageid):
	'''
	:param service: The gmail service variable used to access the gmail account
	:param messageid: The id of the email you want me to retrieve
	:return: A dict with the email information. WIll return None if we couldn't grab the mail
	'''
	#This will attempt to get the single email 3 times
	email = None
	for i in range(0,3):
		try:
			email = service.users().messages().get(userId='me', id=messageid).execute()
			break
		except googleapiclient.errors.HttpError:
			time.sleep(2)
	return email

def deleteemail(service, messageid):
	'''
	:param service: The gmail service variable used to access the gmail account
	:param message: The id of the email you want me to delete
	:return: None
	'''
	#This will attempt to delete the email with the messageid three times
	for i in range(0,3):
		try:
			service.users().messages().delete(userId='me', id=messageid).execute()
			break
		except googleapiclient.errors.HttpError:
			time.sleep(2)

def markasread(service, messageid):
	'''
		:param service: The gmail service variable used to access the gmail account
		:param message: The id of the email you want me to mark as read
		:return: None
	'''
	#Attepts to marks email with the messageid as read 3 times.
	for i in range(0,3):
		try:
			service.users().messages().modify(userId='me', id=messageid,body={'removeLabelIds': ['UNREAD']}).execute()
			break
		except googleapiclient.errors.HttpError:
			time.sleep(2)
			
def createmessage(sender,to,subject,bodytext):
	'''
	:param sender:  Who is we
	:param to: Who we sending this carp to
	:param subject: What be thynn subject
	:param bodytext: What might thynn text be?
	:return: Thynn message var
	'''
	message = MIMEText(bodytext)
	message['to'] = to
	message['from'] = sender
	message['subject'] = subject
	return {'raw': base64.urlsafe_b64decode(message.as_bytes())}

def sendmessage(service, message):
	for i in range(0,3):
		try:
			service.users().messages().send(userID='me', body=message).execute()
			break
		except googleapiclient.errors.HttpError:
			print("Opsi woopsi")
			time.sleep(2)
def getemailfromstring(emailusertext):
	'''
	:param emailusertext: The gmail email string needing to be processed
	:return: The raw email address
	'''
	emaillist = list(emailusertext)
	try:
		firstlsign = emaillist.index("<")+1
		lastlsign = emaillist.__len__()-1
		return ''.join(emaillist[firstlsign:lastlsign])
	except ValueError:
		return emailusertext
		