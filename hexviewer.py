# coding: utf-8

import datetime, os, ui

def button_action(sender):
    global pos, searchstr, view
    tvd = view['tv_data']
    tfss = view['tf_search_str']
    if tfss.text != '':
        if tfss.text == searchstr:
            #next hit
            pos = tvd.text.find(searchstr,pos+1)
        else:
            #new search
            searchstr = tfss.text
            pos = tvd.text.find(searchstr)
        if pos >= 0:    #hit
            x = tvd.text.find('\n',pos) - 79        #line start
            y = len(tvd.text) - len(tvd.text) % 80  #last line start
            if pos < y:
                sender.title = tvd.text[x:x+10]
            else:
                sender.title = tvd.text[y:y+10]
            tvd.selected_range = (pos, pos+len(searchstr))  # works only when textview is active!!!
        else:
            sender.title = 'Restart'
    else: 
        sender.title = 'Search'

def get_dir(path):
    dirs  = [] if path == root else ['..']
    files = []
    for entry in sorted(os.listdir(path)):
        if os.path.isdir(path + '/' + entry):
            dirs.append(entry)
        else:
            files.append(entry)
    all = ['/' + dir for dir in dirs]
    for file in files:
        full_pathname = path + '/' + file
        size = '{} Bytes'.format(os.path.getsize(full_pathname))
        date = datetime.datetime.fromtimestamp(os.path.getmtime(full_pathname))
        all.append('{:43} | {:20} | {}'.format(file, size, date))
    return all

def table_tapped(sender):
    global path, tableview1, view, buffer
    rowtext = sender.items[sender.selected_row]
    filename_tapped = rowtext.partition('|')[0].strip()
    if rowtext[0] == '/':
        if filename_tapped == '/..':
            pos = path.rfind('/')
            path = path[:pos]
        else:
            path = path + filename_tapped
        all = get_dir(path)
        view.name = path
        tableview1.close()
        tableview1 = make_tableview1(view)
        lst = ui.ListDataSource(all)
        tableview1.data_source = lst
        tableview1.delegate = lst
        lst.font = ('Courier',18)
        lst.action = table_tapped
        lst.delete_enabled = False
        return
    filename = filename_tapped
    tableview1.hidden = True
    tableview1.close()
    textview1 = ui.TextView()
    textview1.name = 'tv_data'
    textview1.frame = view.frame
    textview1.x = 6
    textview1.y = 46
    textview1.width = view.width - 12
    textview1.height = view.height - 52
    textview1.autoresizing = 'WHT'
    #textview1.editable = False     #easy access no double tap needed
    textview1.font = ('Courier', 15)
    view.add_subview(textview1)
    textfield1 = ui.TextField()
    textfield1.name = 'tf_search_str'
    textfield1.x = textfield1.y = 6
    textfield1.width = view.width - 161
    textfield1.height = 32
    textfield1.flex = 'WR'
    view.add_subview(textfield1)
    button1 = ui.Button()
    button1.name = 'btn_search'
    button1.title = 'Search'
    button1.x = view.width - 149
    button1.y = 6
    button1.width = 144
    button1.height = 32
    button1.flex = 'WL'
    button1.border_width = 2
    button1.corner_radius = 5
    button1.action = button_action
    view.add_subview(button1)
    view.name = filename
    full_pathname = path + '/' + filename
    try:
        with open(full_pathname,'rb') as in_file:
            for line in range(0, os.path.getsize(full_pathname), 16):
                h = s = ''
                for c in in_file.read(16):
                    i = ord(c)
                    h += '{:02X} '.format(i)
                    s += c if 31 < i < 127 else '.'
                buffer += '0x{:08X} | {:48}| {:8}\n'.format(line, h, s)
            textview1.text = buffer
    except:
        textview1.text = 'Error!\nFile = ' + full_pathname

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

pos = -1
searchstr = ''
buffer = ''
tvd = None 
tfss = None 
root = os.path.expanduser('~')
path = os.getcwd()
all = get_dir(path)
pos = path.rfind('/')
cpath = path[pos:]

view = ui.View()
view.name = path
view.x = view.y = 0
view.width = 768
view.height = 960
view.background_color = 'white'
tableview1 = make_tableview1(view)
lst = make_lst(tableview1, all)
view.present('fullscreen')