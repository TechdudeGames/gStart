import googleapiclient.errors
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
			i = 4 #A sneaky roundabout way of stopping the loop if we got it the first time
		except googleapiclient.errors.HttpError:
			pass
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
			i = 4
		except googleapiclient.errors.HttpError:
			pass
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
			i = 4
		except googleapiclient.errors.HttpError:
			pass

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
			i = 4
		except googleapiclient.errors.HttpError:
			pass