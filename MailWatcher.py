#!/usr/bin/python3
import gStartBackend
import xml.etree.cElementTree as elementtree
import os
import sys
import time
import multiprocessing
continuetorun = True
arguments = sys.argv[1:]
itterationsperclear = 20
sendfeedbackemails = False
mailcheckdelay = 30
print("===MailWatcher===\n"
      "TechdudeGames Inc.\n"
      "Version 1.1\n")
if arguments != []:
	try:
		helparg = arguments.index("-h")
		print(""
		      "-c | Number of iterations before I clear the screen\n"
		      "-t | Times between mail checks"
		      "-h | prints this help thing :)\n"
		      "-s | Send email feedback if the pass is right or if the server is already running"
		      "-r | random crap ;)\n")
		continuetorun = False
	except ValueError:
		try:
			ipcfarg = arguments.index("-c")
			try:
				ipcfarg_perm = arguments[ipcfarg+1]
				itterationsperclear = float(ipcfarg_perm)
			except IndexError:
				print("Invalid perameter")
				continuetorun = False
			except IndexError:
				print("Invalid perameter")
				continuetorun = False
		except ValueError:
			pass
		
		try:
			timearg = arguments.index("-t")
			try:
				timearg_perm = arguments[timearg+1]
				mailcheckdelay = float(timearg_perm)
			except IndexError:
				print("Invalid perameter")
				continuetorun = False
			except IndexError:
				print("Invalid perameter")
				continuetorun = False
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
	
stopidle =  multiprocessing.Value('i', 0)
def idlingemailsender(stopvar):
	while stopvar.value == 1:
		pass
idle_proc = multiprocessing.Process(target=idlingemailsender, args=[stopidle])
counter = 0
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
				stopidle.value = 1
				idle_proc.start()
				os.chdir(serverdir)
				os.system(servercommand)
				os.chdir(origpath)
				gStartBackend.deletecorrectpassemail(allowed_senders, serverpass)
				stopidle.value = 0
				while idle_proc.is_alive():
					pass
				stopidle.value = 0
			time.sleep(mailcheckdelay)
			couter += 1
			if counter == itterationsperclear:
				os.system("clear")
else:
	print("Yo dawg you need to data.xml")
