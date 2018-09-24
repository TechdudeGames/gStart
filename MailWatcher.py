#!/usr/bin/python3
import gStartBackend
import xml.etree.cElementTree as elementtree
import os
import sys
import time
import multiprocessing
continuetorun = True
arguments = sys.argv[1:]
itterationsperclear = 2880
sendfb = True
mailcheckdelay = 1
stoppass = "ST0P"
print("===MailWatcher===\n"
      "TechdudeGames Inc.\n"
      "Version 1.5\n")
#Command line arguments
if arguments != []:
	if "-h" in arguments:
		print(""
		      "-h | prints this help thing :)\n"
		      "-c | Number of iterations before I clear the screen\n"
		      "-t | Times between mail checks\n"
		      "-s | Send email feedback if the pass is right or if the server is already running. Default is 1 (On) and 0 is Off\n"
		      "-r | random crap ;)\n")
		continuetorun = False
	else:
		if "-c" in arguments:
			ipcfarg = arguments.index("-c")
			try:
				ipcfarg_perm = arguments[ipcfarg+1]
				itterationsperclear = float(ipcfarg_perm)
			except IndexError:
				print("Invalid perameter")
				continuetorun = False
	
		if "-f" in arguments:
			timearg = arguments.index("-t")
			try:
				timearg_perm = arguments[timearg+1]
				mailcheckdelay = float(timearg_perm)
			except IndexError:
				print("Invalid perameter")
				continuetorun = False
	
		if "-s" in arguments:
			sendarg= arguments.index("-s")
			sendarg_perm = arguments[sendarg+1]
			if sendarg_perm == 0:
				sendfb = False
	
		if "-r" in arguments:
				print("A skunk sat on a stump\n"
			          "The stump thunk\n"
			          "The skunk thump\n"
			          "The stump thunk the skunk stunk\n"
			          "The skunk thunk the stump stunk\n")
				continuetorun = False
			
	
#This is the idler that starts the server. It is on a separate thread to allow us to check for correct emails while
#This guy is waiting for the server to stop.
def idler():
	os.chdir(serverdir)
	os.system(servercommand)
	os.chdir(origpath)
idle_proc = multiprocessing.Process(target=idler)
counter = 0
if (os.path.isfile('data.xml')):
	if continuetorun:
		authfile = elementtree.ElementTree(file="data.xml")
		authroot = authfile.getroot()
		# Getting the password and availible senders
		allowed_senders = []
		serverpass = []
		servercommand = None
		serverdir = None
		serverport = None
		for tag in authroot:
			if tag.tag == "directory":
				serverdir = tag.text
			if tag.tag == "pass":
				serverpass.append(tag.text)
			if tag.tag == "command":
				servercommand = tag.text
			if tag.tag == "allowed_email":
				allowed_senders.append(tag.text)
			if tag.tag == "port":
				serverport = tag.text
		serverpass.append(stoppass)
		origpath = os.getcwd()
		#Main loop of dis bad boi.
		keeponloopin = True
		while keeponloopin:
			gmailresult = gStartBackend.getmails(valid_senders=allowed_senders,valid_passwords=stoppass,verbose=True)
			#We shove the result of ^ into gmailresult
			if gmailresult['passes'].__len__() >0:
				if stoppass in gmailresult['passes']:
					keeponloopin = False
					print("Stopping now")
				else:
					'''
					This next part is purly to prevent a freak issue from occuring if two people were to
					simaltaniously send two emails with two different correct passwords.
					'''
					firstpass = gmailresult['passes'][0]
					singlepass = True
					for checkingpass in gmailresult['passes'][0:]:
						if firstpass != checkingpass:
							singlepass = False
					
					if singlepass:
						# If we only have one password
						gStartBackend.sendemailcorrectpass(recipients=gmailresult['senders'], servername="Hahlol",
						                                   port_number=serverport)
						gStartBackend.deletevalidemails(idlist=gmailresult["ids"])
						while idle_proc.is_alive():
							pass
						idle_proc.start()
						while idle_proc.is_alive():
							gmailresult = gStartBackend.getmails(valid_senders=allowed_senders,
							                                     valid_passwords=list((serverpass, "DirtTech1")),
							                                     verbose=True)
							gStartBackend.deletevalidemails(idlist=gmailresult["ids"])
							gStartBackend.sendemailidlemode(recipients=gmailresult['senders'], port_number=serverport)
							time.sleep(mailcheckdelay)
						
						gmailresult = gStartBackend.getmails(valid_senders=allowed_senders,
						                                     valid_passwords=list(serverpass, "DirtTech1"),
						                                     verbose=True)
						gStartBackend.deletevalidemails(idlist=gmailresult["ids"])
					else:
						# We send an email to everyone if we have the rare condition described above.
						gStartBackend.deletevalidemails(idlist=gmailresult["ids"])
						gStartBackend.sendmultipassemail(recipients=gmailresult['senders'])
			time.sleep(mailcheckdelay)
			counter += 1
			if counter == itterationsperclear:
				os.system("clear")
				counter = 0
else:
	print("Yo dawg you need the data.xml. Please use Manager to create one.")
