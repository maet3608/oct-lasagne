"""
Constants for button labelsl, key codes and so on.
"""

from kivy.metrics import dp

# Prefix for layer annotation columns in pandas dataframe
PREFIX = 'l:'

# Files
BACKUPFILE = 'backup.csv'
ANNOFILE = 'annotation.pkl'
OCTEXT = '.npy'

# Columns
OCTID = 'oct_id'
LAYERS = ['l:ILM', 'l:RNFL', 'l:GCL', 'l:IPL', 'l:INL', 'l:OPL',
          'l:ONL', 'l:PR', 'l:RPE', 'l:BM']

# Size of application main window
WINDOWSIZE = (dp(700), dp(800))

# Key codes
KEYSHIFT = 304
KEYCTRL = 308
KEYALT = 305
KEYPAGEUP = 280
KEYPAGEDOWN = 281
KEYUP = 273
KEYDOWN = 274
KEYLEFT = 276
KEYRIGHT = 275
KEYLV = 118  # lowercase v
KEYLA = 97  # lowercase a

# Button sizes
BTNSIZE = (dp(100), dp(30))
BTNHINT = (None, None)
FNTSIZE = dp(14)
FNTSMALLSIZE = dp(12)
BTNHEIGHT = dp(25)

# Popup dialogs
POPSMALLSIZE = (dp(400), dp(90))
POPLARGESIZE = (dp(300), dp(400))

# Button labels
BTNANNO = 'Annotation'
BTNLAYER = 'Layer'
BTNFILTER = 'Filter...'
BTNADDLAYER = 'Add layer...'
BTNDELLAYER = 'Del layer...'
BTNSAVE = 'Save'
BTNRECOVER = 'Load backup'
BTNAUTOSAVE = {True: 'Autosave ON', False: 'Autosave OFF'}
BTNISVISIBLE = {True: 'Show layer ON', False: 'Show layer OFF'}
BTNVIEWALL = {True: 'Show all ON', False: 'Show all OFF'}

# Editor modes
EDITOFF = 'off'
EDITADD = 'add'
EDITDEL = 'del'
EDITMOVE = 'move'
EDITMODES = {KEYCTRL: EDITADD, KEYALT: EDITMOVE, KEYSHIFT: EDITDEL}
