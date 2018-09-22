#!/usr/bin/python3
import tkinter as tk
from tkinter import messagebox
import pygubu
import os
import xml.etree.cElementTree as ET
from xml.dom import minidom
import platform
class managergui:
	def __init__(self, master):
		current = os.getcwd()
		# Now for the window stuff
		self.master = master
		# 1: Create a builder
		self.builder = builder = pygubu.Builder()
		builder.add_from_file(os.path.join(current, "gui", "manager.ui"))
		self.mainwindow = builder.get_object('GUI', master)
		#Get the xml carp
		if (os.path.isfile("data.xml")) != True:
			messagebox.showwarning(title="Missing data.xml",
			                                  message="We could not find the data.xml file, creating it now.")
			dataroot = ET.Element("data")
			ET.SubElement(dataroot, "pass").text = "abc123"
			ET.SubElement(dataroot, "directory").text = "./"
			ET.SubElement(dataroot, "command").text = "./start.sh"
			ET.SubElement(dataroot, "port").text = "8080"
			ET.SubElement(dataroot, "allowed_email").text = "test &lt;testmail@test.com&gt;"
			xmlstr = minidom.parseString(ET.tostring(dataroot)).toprettyxml(indent="    ")
			with open("data.xml", "w") as write:
				write.write(xmlstr)
				write.close()
		datafile = ET.ElementTree(file="data.xml")
		dataroot = datafile.getroot()
		# Getting the password and availible senders
		allowed_senders = []
		serverpass = None
		servercommand = None
		serverdir = None
		serverport = None
		for tag in dataroot:
			if tag.tag == "directory":
				serverdir = tag.text
			if tag.tag == "pass":
				serverpass = tag.text
			if tag.tag == "command":
				servercommand = tag.text
			if tag.tag == "allowed_email":
				allowed_senders.append(tag.text)
			if tag.tag == "port":
				serverport = tag.text
		#Update the GUI to show the data carp
		builder.get_variable("serverpass").set(serverpass)
		builder.get_variable("fullcmd").set(serverdir + servercommand)
		builder.get_variable("currentport").set(serverport)
		callbacks = {
			"changepass": None,
			"changecmd": None,
			"changeport": None
		}
		builder.connect_callbacks(self)
		builder.connect_callbacks(callbacks)
	
	def changepass(self):
		newpass = self.builder.get_variable("newpass").get()
		if newpass.__len__() > 0:
			serverpass_parse = ET.parse("data.xml")
			serverpass_elm = serverpass_parse.findall("pass")[0]
			serverpass_elm.text = newpass
			serverpass_parse.write("data.xml")
			self.builder.get_variable("pass").set(newpass)
		else:
			messagebox.showerror(title="Error", message="I am not about to let you have a null password.")
	
	def changeport(self):
		newport = self.builder.get_variable("newport").get()
		serverport_parse = ET.parse("data.xml")
		if serverport_parse.findall("port").__len__() != 0:
			try:
				if newport.__len__() > 5:
					confirmlargeport = messagebox.askyesno(title="Confirm Large Port",
					                                       message="Are you sure you want a large port #?")
					if confirmlargeport:
						serverport_elm = serverport_parse.findall("port")[0]
						serverport_elm.text = str(int(newport))
						serverport_parse.write("data.xml")
						self.builder.get_variable("currentport").set(newport)
				elif newport.__len__() < 6:
					serverport_elm = serverport_parse.findall("port")[0]
					serverport_elm.text = str(int(newport))
					serverport_parse.write("data.xml")
					self.builder.get_variable("currentport").set(newport)
			except ValueError:
				if newport == "":
					snarkyremark = "Sorry sir/mam, no blank ports."
					messagebox.showerror(title="Error", message=snarkyremark)
				else:
					snarkyremark = "Last time I checked " + self.builder.get_variable(
						"newport").get() + " is not a valid port."
					messagebox.showerror(title="Error", message=snarkyremark)
		else:
			messagebox.showerror(title="Error", message="The data.xml file does not contain the port tag")
	
	def changecmd(self):
		fullcmd = self.builder.get_variable("newcmd").get()
		if fullcmd.__len__() > 0:
			fullcmdlist = list(fullcmd)
			fullcmdlist.reverse()
			if platform.win32_ver() == ('', '', '', ''):
				lastslash = fullcmdlist.index("/")
			else:
				lastslash = fullcmdlist.index("\\")
			onlycmd = fullcmdlist[:lastslash]
			onlycmd.reverse()
			if platform.win32_ver() == ('', '', '', ''):
				onlycmd.insert(0, "./")
			else:
				lastslash = fullcmdlist.index(".\\")
			cmd = ''.join(onlycmd)
			onlypath = fullcmdlist[lastslash:]
			onlypath.reverse()
			path = ''.join(onlypath)
			serverdir_parse = ET.parse("data.xml")
			serverdir_elm = serverdir_parse.findall("directory")[0]
			serverdir_elm.text = path
			serverdir_parse.write("data.xml")
			#
			servercmd_parse = ET.parse("data.xml")
			servercmd_elm = servercmd_parse.findall("command")[0]
			servercmd_elm.text = cmd
			servercmd_parse.write("data.xml")
			self.builder.get_variable("fullcmd").set(path + cmd)
		else:
			messagebox.showerror(title="Invalid command", message="Dude, you can't have an empty cmd bro.")


if __name__ == '__main__':
	root = tk.Tk()
	root.title("Manager GUI")
	app = managergui(root)
	root.mainloop()