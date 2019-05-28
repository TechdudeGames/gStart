#!/usr/bin/python3
import json
import multiprocessing
import os
import sys
import time
import signal

def cleanexit(sig, frame):
	print("\nStopping...")
	sys.exit()


signal.signal(signal.SIGINT, cleanexit)  # Catches ^c and stops

from gStartBackend import backendfunctions

backend = backendfunctions()
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
		
		if '-t' in arguments:
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


# This is the serverr that starts the server. It is on a separate thread to allow us to check for correct emails while
# This guy is waiting for the server to stop.
def offmainthread(dir, cmd):
	os.chdir(dir)
	os.system(cmd)

backgroundtask_List = []

server_proc = None
counter = 0

if continuetorun:
	# We are clear to run.
	keeponloopin = True  # We assume we are going to continue on with our life unless something comes up
	servernames = []
	serverpasses = []
	serverdirs = []
	servercmds = []
	serverports = []
	backgroundnames= []
	backgroundpasses= []
	backgrounddirs= []
	backgroundcmds= []
	backgroundports = []
	# data.json working crap
	
	if os.path.isfile('data.json'):
		validfile = False
		with open('data.json', 'r') as file:
			try:
				serverdata = json.load(file)
				validfile = True
				file.close()
			except json.decoder.JSONDecodeError:
				# This only occurs if the json file is broken.
				print('Your data.json file is malformed. Please use DataManager to correct this issue.')
		
		if validfile:
			# This portion checks to get the different servers
			if 'servers' in serverdata:
				# This insures that we have a servers portion of the program.
				for tmpserver in serverdata['servers']:
					# tmp server becomes the dictionary with all the needed data.
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
				# This is for when there is no servers tag in the json file
				print('You are missing the servers in the data.json. Please use DataManager to correct this.')
				keeponloopin = False
			
			# This part gets the valid emails
			if 'allowed_emails' in serverdata:
				# Makes sure we have a list of valid emails
				allowed_senders = serverdata['allowed_emails']
			else:
				# This is for when we don't have a email list
				print('The json file is missing the allowed_emails array. Please use DataManager to add one.')
				keeponloopin = False

			if "background_tasks" in serverdata:
				for tmpbackgroundtask in serverdata['background_tasks']:
					# tmp server becomes the dictionary with all the needed data.
					if 'server' in tmpbackgroundtask:
						servernames.append(tmpbackgroundtask['server'])
						backgroundnames.append(tmpbackgroundtask['server'])
					else:
						servernames.append(None)
						backgroundnames.append(None)

					if 'password' in tmpbackgroundtask:
						serverpasses.append(tmpbackgroundtask['password'])
						backgroundpasses.append(tmpbackgroundtask['password'])
					else:
						serverpasses.append(None)
						backgroundpasses.append(None)

					if 'directory' in tmpbackgroundtask:
						serverdirs.append(tmpbackgroundtask['directory'])
						backgrounddirs.append(tmpbackgroundtask['directory'])
					else:
						serverdirs.append(None)
						backgrounddirs.append(None)

					if 'command' in tmpbackgroundtask:
						servercmds.append(tmpbackgroundtask['command'])
						backgroundcmds.append(tmpbackgroundtask['command'])
					else:
						servercmds.append(None)
						backgroundcmds.append(None)

					if 'port' in tmpbackgroundtask:
						serverports.append(tmpbackgroundtask['port'])
						backgroundports.append(tmpbackgroundtask['port'])
					else:
						serverports.append(None)
						backgroundports.append(None)
		
		else:
			keeponloopin = False
	
	else:
		print('You appear to be missing data.json entirely. Please run DataManager to fix this issue.')
		keeponloopin = False
	
	serverpasses.append(stoppass)  # Append the stop password that way it is still in the list.
	while keeponloopin:
		servernumber = 0
		gmailresult = backend.getmail(valid_senders=allowed_senders, valid_passwords=serverpasses, verbose=True)
		# We shove the result of ^ into gmailresult
		if gmailresult['passes'].__len__() > 0:
			
			# Makes sure we actully have results
			if stoppass in gmailresult['passes']:
				keeponloopin = False
				print('Stopping now')
			
			else:
				'''
				This next part is purely to prevent a freak issue from occuring if two people were to
				send two emails with two different correct passwords.
				'''
				firstpass = gmailresult['passes'][0]  # We get the first password we got and compare it to the others
				singlepass = True
				for checkingpass in gmailresult['passes'][1:]:
					if firstpass != checkingpass:
						singlepass = False  # Somehow we have two emails with different passwords. :9

				if singlepass:
					# We only recieved one of a certain pass.
					
					for investigated_server in range(0, servernames.__len__()):
						if gmailresult['passes'][0] == serverpasses[investigated_server]:
							servernumber = investigated_server
					# We find out which server we are going to be starting.
					
					# This portion is only to prevent us from double starting the server_process
					if server_proc:
						if server_proc.is_alive():
							server_proc.join()  # Somehow the server process is running, so we join in to prevent something bad from happening.
					server_proc = multiprocessing.Process(target=offmainthread, args=(serverdirs[servernumber], servercmds[servernumber]))
					# We pass server_proc the things it needs in order to function properly
					
					backend.sendemailcorrectpass(recipients=gmailresult['senders'], servername=servernames[servernumber], port_number=serverports[servernumber])
					backend.deletevalidemails(idlist=gmailresult['ids'])
					print("GOTTE")
					server_proc.start()
					while server_proc.is_alive():
						print("GOTTE")
						# This aims at only running while the server_proc is working
						print("GETTING MAIL")
						gmailresult = backend.getmail(valid_senders=allowed_senders, valid_passwords=backgroundpasses)
						#This it the section where background tasks are checked for and started.
						if gmailresult['passes'].__len__() > 0:
							print("Entering SUBMODE")
							firstpass_background = gmailresult['passes'][0]  # We get the first password we got and compare it to the others
							singlepass_background = True
							for checkingpass in gmailresult['passes'][1:]:
								if firstpass_background != checkingpass:
									singlepass_background = False  # Somehow we have two emails with different passwords. :9

							if singlepass_background:
								for investigated_backgroundtask in range(0, backgroundnames.__len__()):
									if gmailresult['passes'][0] == backgroundpasses[investigated_backgroundtask]:
										backgroundtask_number = investigated_backgroundtask
								backend.sendemailcorrectpassbackground(recipients=gmailresult['senders'], servername=backgroundnames[backgroundtask_number], port_number=backgroundports[backgroundtask_number])
								backend.deletevalidemails(idlist=gmailresult['ids'])

								backgroundtask_List.append(multiprocessing.Process(target=offmainthread, args=(backgrounddirs[backgroundtask_number], backgroundcmds[backgroundtask_number])))
								print("GOTTE1")
								print(backgroundtask_List.__len__())
								backgroundtask_List[backgroundtask_List.__len__()-1].start()
								for tmptask in range(0,backgroundtask_List.__len__()):
									if backgroundtask_List[tmptask].is_alive() != True:
										backgroundtask_List.pop(tmptask)
							# TODO add the else statement for this
						# We again check the mail while the server is running.
						time.sleep(0.5)
						print("otherremove")
						gmailresult = backend.getmail(valid_senders=allowed_senders, valid_passwords=serverpasses)
						backend.deletevalidemails(idlist=gmailresult['ids'])  # We delete the emails with the correct pass.

						backend.sendemailidlemode(recipients=gmailresult['senders'], port_number=serverports[servernumber])

						# We send them and server state email

						time.sleep(mailcheckdelay)
					
					gmailresult = backend.getmail(valid_senders=allowed_senders,
					                              valid_passwords=serverpasses,
					                              verbose=False)
					# We again check the mail to remove any pesky immediate correct password emails
					backend.deletevalidemails(idlist=gmailresult['ids'])
				# We delete those emails
				else:
					# We send an email to everyone if we have the rare condition described above.
					backend.deletevalidemails(idlist=gmailresult['ids'])  # We delete the emails
					backend.sendmultipassemail(recipients=gmailresult['senders'])
		
		time.sleep(mailcheckdelay)
		counter += 1
		if counter == itterationsperclear:
			os.system('clear')
			counter = 0
