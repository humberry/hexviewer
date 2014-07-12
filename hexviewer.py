# coding: utf-8

import datetime, os, ui

def get_dir(path):
    dirs  = [] if path == root else ['..']
    files = []
    for entry in sorted(os.listdir(path)):
        if os.path.isdir(path + '/' + entry):
            dirs.append(entry)
        else:
            files.append(entry)
    #dirs.sort()
    #files.sort()
    #all = []
    #for dir in dirs:
        #namelength = len(dir)
        #all.append('{:89} | <{}>'.format('/' + dir, namelength))
    all = ['/' + dir for dir in dirs]
    for file in files:
        #namelength = len(file)
        full_pathname = path + '/' + file
        size = '{} Bytes'.format(os.path.getsize(full_pathname))
        date = datetime.datetime.fromtimestamp(os.path.getmtime(full_pathname))
        #all.append('{0:43} | {1:20} | {2:} | <{3:}>'.format(file, size, date, namelength))
        all.append('{:43} | {:20} | {}'.format(file, size, date))
    return all

def table_tapped(sender):
    global path, tableview1
    #global lst
    #global tableview1
    #global view
    rowtext = sender.items[sender.selected_row]
    filename_tapped = rowtext.partition('|')[0].strip()
    #start, stop = rowtext.find('<'), rowtext.find('>')
    #namelength = int(rowtext[start+1:stop])
    if rowtext[0] == '/':
        #if rowtext[:namelength+1] == '/..':
        if filename_tapped == '/..':
            pos = path.rfind('/')
            path = path[:pos]
        else:
            path = path + filename_tapped  # rowtext[:namelength+1]
        all = get_dir(path)
        view.name = path
        tableview1.close()
        tableview1 = make_tableview1(view)
        #tableview1 = ui.TableView()
        #tableview1.frame = view.frame
        #tableview1.x = tableview1.y = 0
        #tableview1.flex = 'WH'
        #tableview1.row_height = 30
        #tableview1.background_color = '#DBDBDB'
        #tableview1.allows_selection = True
        #view.add_subview(tableview1)
        lst = ui.ListDataSource(all)
        tableview1.data_source = lst
        tableview1.delegate = lst
        lst.font = ('Courier',18)
        lst.action = table_tapped
        lst.delete_enabled = False
        return
    filename = filename_tapped  # rowtext[:namelength]
    tableview1.hidden = True
    textview1 = ui.TextView()
    textview1.frame = view.frame
    textview1.x = textview1.y = 0
    textview1.autoresizing = 'WH'
    textview1.editable = False
    textview1.font = ('Courier', 15)
    textview1.alignment = ui.ALIGN_LEFT
    view.add_subview(textview1)
    view.name = filename
    try:
        with open(path + '/' + filename,'rb') as in_file:
            buffer = ''
            for line in range(0, os.path.getsize(path + '/' + filename), 16):
                h = s = ''
                for c in in_file.read(16):
                    i = ord(c)
                    h += '{:02X} '.format(i, 'x')
                    s += c if 31 < i < 127 else '.'
                buffer += '0x{:08X} | {:47} | {:8}\n'.format(line, h, s)
            textview1.text = buffer
    except:
        textview1.text = 'Error!\nFile = {}/{}'.format(path, filename)

def make_tableview1(view):
    tableview1 = ui.TableView()
    tableview1.frame = view.frame
    tableview1.x = tableview1.y = 0
    tableview1.flex = 'WH'
    tableview1.row_height = 30
    tableview1.background_color = '#DBDBDB'
    tableview1.allows_selection = True
    view.add_subview(tableview1)
    return tableview1

def make_lst(tableview, all):
    lst = ui.ListDataSource(all)
    tableview.data_source = lst
    tableview.delegate = lst
    tableview.editing = False
    lst.font = ('Courier',18)
    lst.action = table_tapped
    lst.delete_enabled = False
    return lst

root = os.path.expanduser('~')
path = os.getcwd()
all = get_dir(path)
pos = path.rfind('/')
cpath = path[pos:]

view = ui.View()
view.name = path
view.background_color = 'white'
view.flex = 'WH'
tableview1 = make_tableview1(view)
lst = make_lst(tableview1, all)
view.present('fullscreen')
