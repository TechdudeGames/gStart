#!/usr/bin/python3
'''
The only purpose of this program is to allow the management data.json data.
'''
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import gmailworker
import os
import json
import platform
import psutil
#We are going to need to get some emails, so we are going to need some gmail api magic.
SCOPES = 'https://mail.google.com/'
store = file.Storage('token.json')
creds = store.get()
if not creds or creds.invalid:
	flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
	creds = tools.run_flow(flow, store)
service = build('gmail', 'v1', http=creds.authorize(Http()))

print("Email Manager\n"
      "TechdudeGames Inc.")
check_for_mailwatch = True

##while check_for_mailwatch:
#	for current_pid in psutil.pids():
#		proc = psutil.Process(current_pid)
#		proc_data = proc.as_dict()
#Todo, prevent us from continuing if MailWatcher is running.

#

def getmenunumber(minnumber,maxnumber,prompt_text = "\nInput:"):
	keeptrying = True
	attempted_input = ""
	while keeptrying:
		attempted_input = input(prompt_text)
		if attempted_input.isnumeric():
			if float(attempted_input) % 1 == 0.0:
				if (int(attempted_input) <= maxnumber) and (int(attempted_input) >= minnumber):
					keeptrying = False
				else:
					print("Invalid input, try again.")
			else:
				print("Invalid input, try again.")
		else:
			print("Invalid input, try again.")
	return int(attempted_input)

def getnewpath():
	invalid_input = True
	while invalid_input:
		new_path = input("New directory path:")
		if os.path.isdir(os.path.join(new_path)):
			return new_path
		else:
			print("Invalid path, please try again \n")
def getnewfile(startdir):
	invalid_input = True
	while invalid_input:
		file_name = input("Script/Executable Path:")
		if os.path.isfile(os.path.join(startdir, file_name)):
			if platform.win32_ver() == ('', '', '', ''):
				file_name = os.path.join("./", file_name)
			else:
				file_name = os.path.join(".\\", file_name)
			return file_name
		else:
			print("We can't find that file, please try another filename.")




mainmenu = '''
\n
What would you like to do?
1) Manage Servers
2) Manage Emails
3) Quit
'''

servers_submenu = '''
\n
What would you like to do?
1) Display all the current servers
2) Modify a preexisting server
3) Remove a preexisting server
4) Add a new server
5) Go back to the main menu
'''

emails_submenu = '''
What would you like to do?
1) List all the currently accepted senders
2) Add a new email
3) Remove a current email
4) Go back to the main menu
'''
serverdata = None
if not os.path.isfile("data.json"):
	print("You seem to be missing data.json, creating one for you now.")
	serverdata = {"servers": [], "allowed_emails": []}
	with open("data.json", 'w') as datawrite:
		json.dump(serverdata, datawrite, indent=4)
		datawrite.close()

keepongoing = True
with open('data.json', 'r') as file:
	if not serverdata:
		try:
			serverdata = json.load(file)
			file.close()
		except json.decoder.JSONDecodeError:
			# This only occurs if the json file is broken.
			print('Your data.json file is malformed, correcting it now...')
			serverdata = {"servers": [], "allowed_emails": []}
			with open("data.json", 'w') as datawrite:
				json.dump(serverdata, datawrite, indent=4)
				datawrite.close()
if type(serverdata) != dict:
	print("Apparently, the data file is valid, however it has the incorrect starting object.")
	print("Fixing it now by overwriting it with the correct format.")
	serverdata = {"servers": [], "allowed_emails": []}
	with open("data.json", 'w') as datawrite:
		json.dump(serverdata, datawrite, indent=4)
		datawrite.close()

while keepongoing:
	print(mainmenu)
	mainresponse = getmenunumber(1, 3)
	if mainresponse == 1:
		# Doing some
		if "servers" not in serverdata:
			print("Somehow, someway are you missing the entire servers section. I am writing it to the file now.")
			serverdata['servers'] = []
			with open("data.json", 'w') as datawrite:
				json.dump(serverdata, datawrite, indent=4)
				datawrite.close()
		print(servers_submenu)
		servermain_responce = getmenunumber(1, 5)
		# Display server
		if servermain_responce == 1:
			for tmpserverdic in serverdata['servers']:
				if "server" in tmpserverdic:
					print("\nServer Name: ", tmpserverdic['server'])
				else:
					print("\nServerName: ", None)
				if "password" in tmpserverdic:
					print("Password: ", tmpserverdic['password'])
				else:
					print("Password: ", None)
				if "directory" in tmpserverdic:
					print("Directory: ", tmpserverdic['directory'])
				else:
					print("Directory: ", None)
				if "command" in tmpserverdic:
					print("Command: ", tmpserverdic["command"])
				else:
					print("Command: ", None)
				if "port" in tmpserverdic:
					print("Port: ", tmpserverdic['port'])
				else:
					print("Port:", None)
			print("\nPress Enter to continue")
			input()
		
		# Modifing crap
		elif servermain_responce == 2:
			print("Type the server number you wish to modify.")
			for tmpnameindex in range(serverdata['servers'].__len__()):
				print(tmpnameindex, ": ", serverdata['servers'][tmpnameindex]['server'])
			modifing_server = True
			selectedserverindex = getmenunumber(0, serverdata['servers'].__len__())
			while modifing_server:
				# This is serverdata print statements
				# I use an if statement per to make sure I don't get an error
				print("\nType the number of the attrib you wish to modify and press Enter.")
				if "server" in serverdata['servers'][selectedserverindex]:
					print("\n0: Server Name: ", serverdata['servers'][selectedserverindex]['server'])
				else:
					print("\n0: ServerName: ", None)
				if "password" in serverdata['servers'][selectedserverindex]:
					print("1: Password: ", serverdata['servers'][selectedserverindex]['password'])
				else:
					print("1: Password: ", None)
				if "directory" in serverdata['servers'][selectedserverindex]:
					print("2: Directory: ", serverdata['servers'][selectedserverindex]['directory'])
				else:
					print("2: Directory: ", None)
				if "command" in serverdata['servers'][selectedserverindex]:
					print("3: Command: ", serverdata['servers'][selectedserverindex]['command'])
				else:
					print("3: Command: ", None)
				if "port" in serverdata['servers'][selectedserverindex]:
					print("4: Port: ", serverdata['servers'][selectedserverindex]['port'])
				else:
					print("4: Port:", None)
				print("5: Exit modification mode")
				
				attrib_to_modify = getmenunumber(0, 5)
				if attrib_to_modify == 0:
					serverdata['servers'][selectedserverindex]['server'] = input("New name: ")
				
				elif attrib_to_modify == 1:
					serverdata['servers'][selectedserverindex]['password'] = input("New password:")
					if serverdata['servers'][selectedserverindex]['password'].__len__() == 0:
						print("Warning, please know that having no password is a BAD IDEA\n"
						      "Press enter to continue")
						input()
				
				elif attrib_to_modify == 2:
					serverdata['servers'][selectedserverindex]['directory'] = getnewpath()
				
				elif attrib_to_modify == 3:
					# I am only useing a var for this because this can get really long
					startdir = serverdata['servers'][selectedserverindex]['directory']
					serverdata['servers'][selectedserverindex]['command'] = getnewfile(startdir)
				
				elif attrib_to_modify == 4:
					new_port = getmenunumber(0, 99999999999, prompt_text="Type new port number:")
					serverdata['servers'][selectedserverindex]['port'] = new_port
				
				elif attrib_to_modify == 5:
					modifing_server = False
			
			# Change writing
			print("Write out the changes? (1=Yes 2=No)")
			confirm_serverchange = getmenunumber(1, 2)
			if confirm_serverchange == 1:
				with open("data.json", 'w') as datawrite:
					json.dump(serverdata, datawrite, indent=4)
					datawrite.close()
				print("Changes written. Press Enter")
				input()
			else:
				print("Changes not saved. Press Enter")
				input()
		
		elif servermain_responce == 3:
			print("Type the server number you wish to remove.")
			for tmpnameindex in range(serverdata['servers'].__len__()):
				print(tmpnameindex, ": ", serverdata['servers'][tmpnameindex]['server'])
			server_index = getmenunumber(0, serverdata['servers'].__len__())
			print("Are you sure you want to remove this email? (1=Yes 2=No)")
			confirm_server_removal = getmenunumber(1, 2)
			if confirm_server_removal == 1:
				serverdata['servers'].remove(serverdata['servers'][server_index])
				with open("data.json", 'w') as datawrite:
					json.dump(serverdata, datawrite, indent=4)
				print("Server Removed. Press Enter")
				input()
			else:
				print("Removal canceled. Press Enter")
				input()
		
		elif servermain_responce == 4:
			new_server = {}
			new_server['server'] = input("New Server Name: ")
			new_server['password'] = input("Password: ")
			new_server['directory'] = getnewpath()
			new_server['command'] = getnewfile(new_server['directory'])
			new_server['port'] = getmenunumber(0, 99999999999, prompt_text="New port number: ")
			print("\nWrite this new server to the data file? (1=Yes 2=No)")
			confirm_new_server = getmenunumber(1, 2)
			if confirm_new_server == 1:
				serverdata['servers'].append(dict(new_server))
				with open("data.json", 'w') as datawrite:
					json.dump(serverdata, datawrite, indent=4)
					datawrite.close()
			else:
				print("Did not write server to file")
	
	# Mail management
	elif mainresponse == 2:
		if "allowed_emails" not in serverdata:
			print(
				"Somehow, someway are you missing the entire allowed_emails section. I am writing it to the file now.")
			serverdata['allowed_emails'] = []
			with open("data.json", 'w') as datawrite:
				json.dump(serverdata, datawrite, indent=4)
				datawrite.close()
		print(emails_submenu)
		emailsubmenu_input = getmenunumber(1, 4)
		if emailsubmenu_input == 1:
			for tmpemail_index in range(0, serverdata['allowed_emails'].__len__()):
				print(tmpemail_index, ":", serverdata['allowed_emails'][tmpemail_index])
			print("\nPress Enter to continue")
			input()
		
		elif emailsubmenu_input == 2:
			addingemail = True
			print("Please send an email with the text ADDME to the email address MailWatcher uses.")
			print("Press enter when you have done so.")
			input()
			while addingemail:
				gmaildata = gmailworker.getgmailemails(service)
				if gmaildata == None:
					print("We had an error getting the mail, retry? (1=Yes 2=No)")
					continueaddingemail = getmenunumber(1, 2)
					if continueaddingemail == 2:
						addingemail = False
				elif gmaildata['resultSizeEstimate'] == 0:
					print("We can't find any new emails in your inbox. Continue? (1=Yes 2=No)")
					print("(Note): 1 will check for the new emails again.")
					continueaddingemail = getmenunumber(1, 2)
					if continueaddingemail == 2:
						addingemail = False
				else:
					worthysenders = []
					for tmpmailobj in gmaildata['messages']:
						if tmpmailobj != None:
							observed_email = gmailworker.getemaildata(service, tmpmailobj['id'])
							metadata = observed_email['payload']['headers']
							for name_data in metadata:
								if name_data['name'] == 'From':
									if observed_email['snippet'] == "ADDME":
										worthysenders.append(name_data['value'])
										gmailworker.deleteemail(service, tmpmailobj['id'])
					if worthysenders.__len__() == 0:
						print("It appears no emails have the ADDME text in them, retry? (1=Yes 2=No)")
						continueaddingemail = getmenunumber(1, 2)
						if continueaddingemail == 2:
							addingemail = False
					else:
						print("Available Emails:")
						for praisedsender in range(0, worthysenders.__len__()):
							print(praisedsender, ":", worthysenders[praisedsender])
						print("\nPick the number corresponding to the email you want to add.")
						mail_seclection = getmenunumber(0, worthysenders.__len__() - 1)
						if worthysenders[mail_seclection] in serverdata['allowed_emails']:
							print("Silly goose, that email is already on the list :)\n")
							print("Do you want to add another email? (1=Yes 2=No)")
							continueaddingemail = getmenunumber(1, 2)
							if continueaddingemail == 2:
								addingemail = False
						else:
							serverdata['allowed_emails'].append(worthysenders[mail_seclection])
							with open("data.json", 'w') as datawrite:
								json.dump(serverdata, datawrite, indent=4)
								datawrite.close()
							print("Email Added")
							print("Do you want to add another email? (1=Yes 2=No)")
							continueaddingemail = getmenunumber(1, 2)
							if continueaddingemail == 2:
								addingemail = False
		
		elif emailsubmenu_input == 3:
			removing_emails = True
			while removing_emails:
				for tmpemail_index in range(0, serverdata['allowed_emails'].__len__()):
					print(tmpemail_index, ":", serverdata['allowed_emails'][tmpemail_index])
				print("Which email shall I remove")
				remove_email_index = getmenunumber(0, serverdata['allowed_emails'].__len__())
				print("Are you sure you want to remove this email? (1=Yes 2=No)")
				confirmemailremove = getmenunumber(1, 2)
				if confirmemailremove == 1:
					emailtoremove = serverdata['allowed_emails'][remove_email_index]
					while emailtoremove in serverdata['allowed_emails']:
						serverdata['allowed_emails'].remove(emailtoremove)
					with open("data.json", 'w') as datawrite:
						json.dump(serverdata, datawrite, indent=4)
						datawrite.close()
					print("Email Removed")
					print("Do you want to remove another email? (1=Yes 2=No)")
					removingfeedback = getmenunumber(1, 2)
					if removingfeedback == 2:
						removing_emails = False
				else:
					print("Do you want to remove another email? (1=Yes 2=No)")
					removingfeedback = getmenunumber(1, 2)
					if removingfeedback == 2:
						removing_emails = False
	
	elif mainresponse == 3:
		keepongoing = False
#
# Clear crap
# if platform.win32_ver() == ('', '', '', ''):
#	os.system("clear")
# else:
#	os.system("cls")

	
