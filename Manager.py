import tkinter as tk
from tkinter import messagebox
import pygubu
import os
import sys
import xml.etree.cElementTree as elementtree

authfile = elementtree.ElementTree(file="data.xml")
authroot = authfile.getroot()
# Getting the password and availible senders
allowed_senders = []
serverpass = None
servercommand = None
serverdir = None
for tag in authroot:
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
		builder.get_variable('serverpass').set(serverpass)
		callbacks = {
		}
		builder.connect_callbacks(self)
		builder.connect_callbacks(callbacks)
	def changepass(self):
		print(self.builder.get_variable("newpass").get())


if __name__ == '__main__':
	root = tk.Tk()
	root.title("Manager GUI")
	app = managergui(root)
	print(managergui)
	root.mainloop()
