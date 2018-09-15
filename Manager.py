#!/usr/bin/python3
import tkinter as tk
from tkinter import messagebox
import pygubu
import os
import xml.etree.cElementTree as elementtree
import platform
if (os.path.isfile('data.xml')):
	datafile = elementtree.ElementTree(file="data.xml")
	dataroot = datafile.getroot()
	# Getting the password and availible senders
	allowed_senders = []
	serverpass = None
	servercommand = None
	serverdir = None
	for tag in dataroot:
		if tag.tag == "serverdirectory":
			serverdir = tag.text
		if tag.tag == "serverpass":
			serverpass = tag.text
		if tag.tag == "servercommand":
			servercommand = tag.text
		if tag.tag == "allowed_email":
			allowed_senders.append(tag.text)
	
	currentdir = os.getcwd()
	
	
	class managergui:
		def __init__(self, master):
			self.master = master
			# 1: Create a builder
			self.builder = builder = pygubu.Builder()
			builder.add_from_file(os.path.join(currentdir, "gui", "manager.ui"))
			self.mainwindow = builder.get_object('GUI', master)
			builder.get_variable("serverpass").set(serverpass)
			builder.get_variable("fullcmd").set(serverdir+servercommand)
			callbacks = {
				"changepass": None,
				"changecmd" : None
			}
			builder.connect_callbacks(self)
			builder.connect_callbacks(callbacks)
		
		def changepass(self):
			serverpass_parse = elementtree.parse("data.xml")
			serverpass_elm = serverpass_parse.findall("serverpass")[0]
			serverpass_elm.text = self.builder.get_variable("newpass").get()
			serverpass_parse.write("data.xml")
			self.builder.get_variable("fullcmd").set(serverdir+servercommand)
		
		def changecmd(self):
			fullcmd = self.builder.get_variable("newcmd").get()
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
			serverdir_parse = elementtree.parse("data.xml")
			serverdir_elm = serverdir_parse.findall("serverdirectory")[0]
			serverdir_elm.text = path
			serverdir_parse.write("data.xml")
			#
			servercmd_parse = elementtree.parse("data.xml")
			servercmd_elm = servercmd_parse.findall("servercommand")[0]
			servercmd_elm.text = cmd
			servercmd_parse.write("data.xml")
			self.builder.get_variable("fullcmd").set(path+cmd)
	
	
	if __name__ == '__main__':
		root = tk.Tk()
		root.title("Manager GUI")
		app = managergui(root)
		root.mainloop()
else:
	print("I can't find data.xml. uwu")
