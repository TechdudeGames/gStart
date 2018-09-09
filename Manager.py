#!/usr/bin/python3
import tkinter as tk
from tkinter import messagebox
import pygubu
import os
import xml.etree.cElementTree as elementtree
if (os.path.isfile('data.xml')):
	datafile = elementtree.ElementTree(file="data.xml")
	dataroot = datafile.getroot()
	# Getting the password and availible senders
	allowed_senders = []
	serverpass = None
	servercommand = None
	serverdir = None
	for tag in dataroot:
		if tag.tag == "directory":
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
			builder.get_variable("startdir").set(serverdir)
			callbacks = {
				"changepass": None,
				"changedir" : None
			}
			builder.connect_callbacks(self)
			builder.connect_callbacks(callbacks)
		
		def changepass(self):
			serverpass_parse = elementtree.parse("data.xml")
			serverpass_elm = serverpass_parse.findall("serverpass")[0]
			serverpass_elm.text = self.builder.get_variable("newpass").get()
			serverpass_parse.write("data.xml")
			self.builder.get_variable("serverpass").set(self.builder.get_variable("newpass").get())
		
		def changedir(self):
			serverdir_parse = elementtree.parse("data.xml")
			serverdir_elm = serverdir_parse.findall("directory")[0]
			serverdir_elm.text = self.builder.get_variable("newpathdir").get()
			serverdir_parse.write("data.xml")
			self.builder.get_variable("startdir").set(self.builder.get_variable("newpathdir").get())
	
	
	if __name__ == '__main__':
		root = tk.Tk()
		root.title("Manager GUI")
		app = managergui(root)
		root.mainloop()
else:
	print("I can't find data.xml. uwu")
