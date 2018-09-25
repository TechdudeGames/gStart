#!/usr/bin/python3
import gStartBackend
import json
import os
import sys
import time
import multiprocessing

continuetorun = True
arguments = sys.argv[1:]
itterationsperclear = 2880
sendfb = True
mailcheckdelay = 1
stoppass = 'ST0P'
origpath = os.getcwd()
print('===MailWatcher===\n'
      'TechdudeGames Inc.\n'
      'Version 1.5\n')
# Command line arguments
if arguments != []:
	if '-h' in arguments:
		print(''
		      '-h | prints this help thing :)\n'
		      '-c | Number of iterations before I clear the screen\n'
		      '-t | Times between mail checks\n'
		      '-s | Send email feedback if the pass is right or if the server is already running. Default is 1 (On) and 0 is Off\n'
		      '-r | random crap ;)\n')
		continuetorun = False
	else:
		if '-c' in arguments:
			ipcfarg = arguments.index('-c')
			try:
				ipcfarg_perm = arguments[ipcfarg + 1]
				itterationsperclear = float(ipcfarg_perm)
			except IndexError:
				print('Invalid perameter')
				continuetorun = False
		
		if '-f' in arguments:
			timearg = arguments.index('-t')
			try:
				timearg_perm = arguments[timearg + 1]
				mailcheckdelay = float(timearg_perm)
			except IndexError:
				print('Invalid perameter')
				continuetorun = False
		
		if '-s' in arguments:
			sendarg = arguments.index('-s')
			sendarg_perm = arguments[sendarg + 1]
			if sendarg_perm == 0:
				sendfb = False
		
		if '-r' in arguments:
			print('A skunk sat on a stump\n'
			      'The stump thunk\n'
			      'The skunk thump\n'
			      'The stump thunk the skunk stunk\n'
			      'The skunk thunk the stump stunk\n')
			continuetorun = False


# This is the idler that starts the server. It is on a separate thread to allow us to check for correct emails while
# This guy is waiting for the server to stop.
def idler(dir, cmd):
	os.chdir(dir)
	os.system(cmd)
	os.chdir(origpath)


idle_proc = None
counter = 0

if continuetorun:
	keeponloopin = True
	servernames = []
	serverpasses = []
	serverdirs = []
	servercmds = []
	serverports = []
	# data.json working crap
	if os.path.isfile('data.json'):
		validfile = False
		with open('data.json', 'r') as file:
			try:
				serverdata = json.load(file)
				validfile = True
			except json.decoder.JSONDecodeError:
				print('Your data.json file is malformed.')
		
		if validfile:
			# This portion checks to get the different servers
			if 'servers' in serverdata:
				for tmpserver in serverdata['servers']:
					if 'server' in tmpserver:
						servernames.append(tmpserver['server'])
					else:
						servernames.append(None)
						
					if 'password' in tmpserver:
						serverpasses.append(tmpserver['password'])
					else:
						serverpasses.append(None)
						
					if 'directory' in tmpserver:
						serverdirs.append(tmpserver['directory'])
					else:
						serverdirs.append(None)
					
					if 'port' in tmpserver:
						serverports.append(tmpserver['port'])
					else:
						serverports.append(None)
					
			
			else:
				print('You are missing the servers in the data.json. Please correct this.')
				keeponloopin = False
			
			
			
			
			
			
			
			# This portion gets the valid emails
			if 'allowed_emails' in serverdata:
				allowed_senders = serverdata['allowed_emails']
			else:
				print('The json file is missing the allowed_emails array. Please add it to continue')
				keeponloopin = False
		
		else:
			keeponloopin = False
	
	else:
		print('You appear to be missing data.json entirely.')
		keeponloopin = False
	
	# Main loop of dis bad boi.
	
	while keeponloopin:
		gmailresult = gStartBackend.getmails(valid_senders=allowed_senders, valid_passwords=stoppass, verbose=True)
		# We shove the result of ^ into gmailresult
		if gmailresult['passes'].__len__() > 0:
			if stoppass in gmailresult['passes']:
				keeponloopin = False
				print('Stopping now')
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
					for investigated_server in range(0,servernames.__len__()-1):
							if gmailresult['passes'][0] == serverpasses[investigated_server]:
								servernumber = investigated_server
					if idle_proc:
						while idle_proc.is_alive():
							pass
					else:
						idle_proc = multiprocessing.Process(target=idler, args=(serverdirs[servernumber], servercmds[servernumber]))
					# If we only have one password
					gStartBackend.sendemailcorrectpass(recipients=gmailresult['senders'], servername=servernames[servernumber],
					                                   port_number=serverdirs[servernumber])
					gStartBackend.deletevalidemails(idlist=gmailresult['ids'])
					idle_proc.start()
					while idle_proc.is_alive():
						gmailresult = gStartBackend.getmails(valid_senders=allowed_senders,
						                                     valid_passwords=list((serverpasses, 'DirtTech1')),
						                                     verbose=True)
						gStartBackend.deletevalidemails(idlist=gmailresult['ids'])
						gStartBackend.sendemailidlemode(recipients=gmailresult['senders'], port_number=serverdirs[servernumber])
						time.sleep(mailcheckdelay)
					
					gmailresult = gStartBackend.getmails(valid_senders=allowed_senders,
					                                     valid_passwords=list(serverpasses, 'DirtTech1'),
					                                     verbose=True)
					gStartBackend.deletevalidemails(idlist=gmailresult['ids'])
					idle_proc = None
				else:
					# We send an email to everyone if we have the rare condition described above.
					gStartBackend.deletevalidemails(idlist=gmailresult['ids'])
					gStartBackend.sendmultipassemail(recipients=gmailresult['senders'])
		time.sleep(mailcheckdelay)
		counter += 1
		if counter == itterationsperclear:
			os.system('clear')
			counter = 0
