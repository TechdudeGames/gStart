import gStartBackend
import xml.etree.cElementTree as elementtree
import os
import time
authfile = elementtree.ElementTree(file="data.xml")
authroot = authfile.getroot()
#Getting the password and availible senders
allowed_senders = []
serverpass = None
servercommand = None
for tag in authroot:
	if tag.tag == "serverpass":
		serverpass = tag.text
	if tag.tag == "servercommand":
		servercommand = tag.text
	if tag.tag == "allowed_email":
		allowed_senders.append(tag.text)
serveroffline = True
while True:
	needtostart = gStartBackend.checkmail(allowed_senders, serverpass)
	if needtostart:
		os.system("screen %s" % servercommand)
		needtostart = False
		gStartBackend.checkmail(allowed_senders, serverpass)
		#Insures that any email with the password that was sent with the password is not going to retrigger the server immediatly
	time.sleep(30)