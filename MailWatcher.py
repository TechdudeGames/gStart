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
serverdir = None
for tag in authroot:
	if tag.tag == "directory":
		serverdir = tag.text
	if tag.tag == "serverpass":
		serverpass = tag.text
	if tag.tag == "servercommand":
		servercommand = tag.text
	if tag.tag == "allowed_email":
		allowed_senders.append(tag.text)
origpath = os.getcwd()
while True:
	needtostart = gStartBackend.checkmail(allowed_senders, serverpass)
	if needtostart:
		os.chdir(serverdir)
		os.system(servercommand)
		needtostart = False
		os.chdir(origpath)
		gStartBackend.markcorrectpassemail(allowed_senders, serverpass)
		time.sleep(5)
		#Insures that any email with the password that was sent with the password is not going to retrigger the server immediatly
	time.sleep(30)
