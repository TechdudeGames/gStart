import tkinter as tk
from tkinter import messagebox
import pygubu
import os
import sys
import xml.etree.cElementTree as elementtree

#GUI class
class managergui(pygubu.TkApplication):
	def _create_ui(self):
		# 1: Create a builder
		self.builder = builder = pygubu.Builder()
		# 2: Load an ui file
		builder.add_from_file('gui/' + 'manager.ui')
		self.toplevel = builder.get_object('GUI', self.master)
root = tk.Tk()
app = managergui(root)
app.run()