# coding: utf-8

import ui
import os
import datetime
import sys

def get_dir(path):
	verz = os.listdir(path)
	if path == root:
		dirs = []
	else:
		dirs = ['..']
	files = []
	for entry in verz:
		if os.path.isdir(path + '/' + entry):
			dirs.append(entry)
		else:
			files.append(entry)
	dirs.sort()
	files.sort()
	all = []
	for dir in dirs:
		namelength = len(dir)
		all.append('{:89} | <{}>'.format('/' + dir, namelength))
	for file in files:
		namelength = len(file)
		size = str(os.path.getsize(path + '/' + file)) + ' Bytes'
		date = datetime.datetime.fromtimestamp(os.path.getmtime(path + '/' + file))
		all.append('{0:44} | {1:20} | {2:} | <{3:}>'.format(file, size, date, namelength))
	return all

def table_tapped(sender):
	global path
	global lst
	global tableview1
	global view
	rowtext = sender.items[sender.selected_row]
	start = rowtext.find('<')
	stop = rowtext.find('>')
	namelength = int(rowtext[start+1:stop])
	if rowtext[0] == '/':
		if rowtext[:namelength+1] == '/..':
			pos = path.rfind('/')
			path = path[:pos]
		else:
			path = path + rowtext[:namelength+1]
		all = get_dir(path)
		view.name = path
		tableview1.close()
		tableview1 = ui.TableView()
		tableview1.x = 0
		tableview1.y = 0
		tableview1.height = view.height
		tableview1.width = view.width
		tableview1.center = (view.width * 0.5, view.height * 0.5)
		tableview1.flex = 'WH'
		tableview1.row_height = 30
		tableview1.background_color = '#DBDBDB'
		tableview1.allows_selection = True
		view.add_subview(tableview1)
		lst = ui.ListDataSource(all)
		tableview1.data_source = lst
		tableview1.delegate = lst
		lst.font = ('Courier',18)
		lst.action = table_tapped
		lst.delete_enabled = False 
		return
	filename = rowtext[:namelength]
	tableview1.hidden = True
	textview1 = ui.TextView()
	textview1.x = 0
	textview1.y = 0
	textview1.width = view.width
	textview1.height = view.height
	textview1.autoresizing = 'WH'
	textview1.editable = False
	textview1.font = ('Courier', 15)
	textview1.alignment = ui.ALIGN_LEFT
	view.add_subview(textview1)
	view.name = filename
	try:
		file = open(path + '/' + filename,'rb')
		for line in range(0, os.path.getsize(path + '/' + filename), 16):
			h = ''
			s = ''
			data = file.read(16)
			for c in data:
				i = ord(c)
				h += '{:02X}'.format(i, 'x') + ' '
				if (31 < i < 127):
					s += chr(i)
				else:
					s += '.'
			textview1.text += '0x{:08X} | {:47} | {:8}'.format(line, h, s) + '\n'
		file.close()
	except:
		textview1.text = 'Error!\nFile = ' + path + '/' + filename

root = os.path.expanduser('~')
path = os.getcwd()
all = get_dir(path)
pos = path.rfind('/')
cpath = path[pos:]

view = ui.View()
view.name = path
view.background_color = 'white'
view.flex = 'WH'
tableview1 = ui.TableView()
tableview1.center = (view.width * 0.5, view.height * 0.5)
tableview1.flex = 'WH'
tableview1.row_height = 30
tableview1.background_color = '#DBDBDB'
tableview1.allows_selection = True
view.add_subview(tableview1)
lst = ui.ListDataSource(all)
tableview1.data_source = lst
tableview1.delegate = lst
tableview1.editing = False
lst.font = ('Courier',18)
lst.action = table_tapped
lst.delete_enabled = False 
view.present('fullscreen')
