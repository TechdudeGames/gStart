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
mailcheckdelay = 30
stoppass = 'ST0P'
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


idle_proc = None
counter = 0

if continuetorun:
	#We are clear to run.
	keeponloopin = True #We assume we are going to continue on with our life unless something comes up
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
				file.close()
			except json.decoder.JSONDecodeError:
				#This only occurs if the json file is broken.
				print('Your data.json file is malformed.')
			
		if validfile:
			# This portion checks to get the different servers
			if 'servers' in serverdata:
				#This insures that we have a servers portion of the program.
				for tmpserver in serverdata['servers']:
					#tmp server becomes the dictionary with all the needed data.
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
						
					if 'command' in tmpserver:
						servercmds.append(tmpserver['command'])
					else:
						servercmds.append(None)
					
					if 'port' in tmpserver:
						serverports.append(tmpserver['port'])
					else:
						serverports.append(None)
			else:
				#This is for when there is no servers tag in the json file
				print('You are missing the servers in the data.json. Please correct this.')
				keeponloopin = False

			#This part gets the valid emails
			if 'allowed_emails' in serverdata:
				#Makes sure we have a list of valid emails
				allowed_senders = serverdata['allowed_emails']
			else:
				#This is for when we don't have a email list
				print('The json file is missing the allowed_emails array. Please add it to continue')
				keeponloopin = False
		
		else:
			keeponloopin = False
	
	else:
		print('You appear to be missing data.json entirely.')
		keeponloopin = False
	
	serverpasses.append(stoppass)  # Append the stop password that way it is still in the list.
	while keeponloopin:
		servernumber = 0
		gmailresult = gStartBackend.getmails(valid_senders=allowed_senders, valid_passwords=serverpasses, verbose=True)
		# We shove the result of ^ into gmailresult
		if gmailresult['passes'].__len__() > 0:

			#Makes sure we actully have results
			if stoppass in gmailresult['passes']:
				keeponloopin = False
				print('Stopping now')

			else:
				'''
				This next part is purly to prevent a freak issue from occuring if two people were to
				simaltaniously send two emails with two different correct passwords.
				'''
				firstpass = gmailresult['passes'][0] #We get the first password we got and compare it to the others
				singlepass = True
				for checkingpass in gmailresult['passes'][0:]:
					if firstpass != checkingpass:
						singlepass = False #Somehow we have two emails with different passwords. :9
				
				if singlepass:
					#We only recieved one of a certain pass.
					
					for investigated_server in range(0,servernames.__len__()):
							if gmailresult['passes'][0] == serverpasses[investigated_server]:
								servernumber = investigated_server
					#We find out which server we are going to be starting.
					
					#This portion is only to prevent us from double starting the idle_process
					if idle_proc:
						if idle_proc.is_alive():
							idle_proc.sjoin() #We join until it is done.
					idle_proc = multiprocessing.Process(target=idler, args=(serverdirs[servernumber], servercmds[servernumber]))
					#We pass idle_proc the things it needs in order to function properly

					gStartBackend.sendemailcorrectpass(recipients=gmailresult['senders'], servername=servernames[servernumber],
					                                   port_number=serverports[servernumber])
					gStartBackend.deletevalidemails(idlist=gmailresult['ids'])
					
					idle_proc.start()
					while idle_proc.is_alive():
						#This aims at only running while the idle_proc is working, but sometimes this can have issues.
						
						gmailresult = gStartBackend.getmails(valid_senders=allowed_senders,
						                                     valid_passwords=list((serverpasses, 'DirtTech1')),
						                                     verbose=False)
						#We again check the mail while the server is running.
						gStartBackend.deletevalidemails(idlist=gmailresult['ids'])#We delete the emails with the correct pass.
						gStartBackend.sendemailidlemode(recipients=gmailresult['senders'], port_number=serverports[servernumber])
						#We send them and idler state email
						time.sleep(mailcheckdelay)

					gmailresult = gStartBackend.getmails(valid_senders=allowed_senders,
					                                     valid_passwords=serverpasses,
					                                     verbose=False)
					# We again check the mail to remove any pesky immediate correct password emails
					gStartBackend.deletevalidemails(idlist=gmailresult['ids'])
					# We delete those emails
				else:
					# We send an email to everyone if we have the rare condition described above.
					gStartBackend.deletevalidemails(idlist=gmailresult['ids']) #We delete the emails
					gStartBackend.sendmultipassemail(recipients=gmailresult['senders'])
					
		time.sleep(mailcheckdelay)
		counter += 1
		if counter == itterationsperclear:
			os.system('clear')
			counter = 0
