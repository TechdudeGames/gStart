#!/usr/bin/python3
import gStartBackend
import xml.etree.cElementTree as elementtree
import os
import sys
import time
continuetorun = True
arguments = sys.argv[1:]
itterationsperclear = 20
print("===MailWatcher===\n"
      "TechdudeGames Inc.\n"
      "Version 1.1\n")
if arguments != []:
	try:
		helparg = arguments.index("-h")
		print(""
		      "-c | Number of iterations before I clear the screen\n"
		      "-h | prints this help thing :)\n"
		      "-r | random crap ;)\n")
		continuetorun = False
	except ValueError:
		try:
			ipcfarg = arguments.index("-c")
			try:
				ipcfarg_perm = arguments[ipcfarg+1]
				itterationsperclear = int(ipcfarg_perm)
			except IndexError:
				print("Invalid perameter")
			except IndexError:
				print("Invalid perameter")
		except ValueError:
			pass
	try:
		if "-r" in arguments:
			print("A skunk sat on a stump\n"
			      "The stump thunk\n"
			      "The skunk thump\n"
			      "The stump thunk the skunk stunk\n"
			      "The skunk thunk the stump stunk\n")
			continuetorun = False
	except ValueError:
		pass
if (os.path.isfile('data.xml')):
	if continuetorun:
		authfile = elementtree.ElementTree(file="data.xml")
		authroot = authfile.getroot()
		# Getting the password and availible senders
		allowed_senders = []
		serverpass = None
		servercommand = None
		serverdir = None
		for tag in authroot:
			if tag.tag == "serverdirectory":
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
				os.chdir(origpath)
				gStartBackend.deletecorrectpassemail(allowed_senders, serverpass)
			# Insures that any email with the password that was sent with the password is not going to retrigger the server immediatly
			time.sleep(30)
else:
	print("Yo dawg you need to data.xml")
