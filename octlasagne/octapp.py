"""
Main window of application
"""

# Disable multi-touch emulation, which frees CTRL key for point movement.
# Also the (confusing) red dots of the touch emulation disappear.
from __future__ import print_function, absolute_import

from kivy.config import Config

# Config.set('kivy', 'log_level', 'error')
Config.set('input', 'mouse', 'mouse,disable_multitouch')

import numpy as np
import pandas as pd
import os.path as osp

from __init__ import __version__
from glob import glob
from datetime import timedelta
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.boxlayout import BoxLayout

from timer import AnnotationTimer
from octpanel import OctPanel
from helptext import HELPTEXT
from common import load_dataframe, save_dataframe, save_as_pickle
from constants import *


class OCTLasagneApp(App):
    """
    Main Kivy application window.
    """

    def __init__(self, config, **kwargs):
        super(OCTLasagneApp, self).__init__(**kwargs)
        self.title = 'oct-lasagne ' + __version__  # App window title
        self.icon = 'icon.ico'
        self.datadir = config['datadir']
        self.ratio = config['ratio']
        self.locked_scans = set(config['locked'])
        self.annopath = osp.join(self.datadir, ANNOFILE)
        self.backuppath = osp.join(self.datadir, BACKUPFILE)
        self.autosave = True  # save annotation on exit
        self.isvisible = True  # toggle visibility of layer annotation
        self.viewall = False  # toggle visibility of all layers
        self.df = None  # Pandas data frame
        self.oct = None  # OCT cube as numpy array of shape n,h,w
        self.oct_id = ''  # name of OCT cube
        self.octidx = -1  # index of OCT currently displayed
        self.scanidx = 0  # index of B scan in OCT currently displayed
        self.dfindex = None  # Pandas row indices currently selected
        self.layername = None  # Layer currently selected for editing

        self.annotimer = AnnotationTimer(self.update_time_display,
                                         self.update_time_anno)

    def build(self):
        """Build the window and its contents"""
        Window.size = WINDOWSIZE
        Window.bind(on_key_down=self.key_down)
        Window.bind(on_key_up=self.key_up)
        Window.bind(on_resize=self.resized)

        def on_dropdown_select(btn):
            return lambda _, x: setattr(btn, 'text', x)

        self.octpanel = OctPanel(self, size=(1000, 1000), do_rotation=False,
                                 auto_bring_to_front=False)

        self.layerdd = DropDown()
        self.layerbtn = Button(text=BTNLAYER, size=BTNSIZE, size_hint=BTNHINT,
                               font_size=FNTSIZE)
        self.layerbtn.bind(on_release=self.layerdd.open)
        self.layerdd.bind(on_select=on_dropdown_select(self.layerbtn))
        self.layerbtn.disabled = True

        self.annodd = DropDown()
        for btname in [BTNFILTER, BTNADDLAYER, BTNDELLAYER, BTNSAVE,
                       BTNRECOVER]:
            btn = Button(text=btname, size_hint_y=None, height=BTNHEIGHT,
                         font_size=FNTSMALLSIZE)
            btn.bind(on_release=self.on_annotation)
            self.annodd.add_widget(btn)
        self.viewallbtn = ToggleButton(text=BTNVIEWALL[self.viewall],
                                       size_hint_y=None, height=BTNHEIGHT,
                                       font_size=FNTSMALLSIZE)
        self.viewallbtn.bind(on_release=self.on_viewall)
        self.annodd.add_widget(self.viewallbtn)
        self.isvisblebtn = ToggleButton(text=BTNISVISIBLE[self.isvisible],
                                        size_hint_y=None, height=BTNHEIGHT,
                                        font_size=FNTSMALLSIZE)
        self.isvisblebtn.bind(on_release=self.on_visible)
        self.annodd.add_widget(self.isvisblebtn)
        self.autosavebtn = ToggleButton(text=BTNAUTOSAVE[self.autosave],
                                        size_hint_y=None, height=BTNHEIGHT,
                                        font_size=FNTSMALLSIZE)
        self.autosavebtn.bind(on_release=self.on_autosave)
        self.annodd.add_widget(self.autosavebtn)
        self.annobtn = Button(text=BTNANNO, size=BTNSIZE, size_hint=BTNHINT,
                              font_size=FNTSIZE)
        self.annobtn.bind(on_release=self.annodd.open)
        self.annodd.bind(on_select=on_dropdown_select(self.annobtn))

        self.nextoctbtn = Button(text='OCT >>', size=BTNSIZE, size_hint=BTNHINT,
                                 font_size=FNTSIZE)
        self.nextoctbtn.bind(on_release=self.on_next_oct)
        self.prevoctbtn = Button(text='<< OCT', size=BTNSIZE, size_hint=BTNHINT,
                                 font_size=FNTSIZE)
        self.prevoctbtn.bind(on_release=self.on_prev_oct)
        self.nextscanbtn = Button(text='Scan >>', size=BTNSIZE,
                                  size_hint=BTNHINT, font_size=FNTSIZE)
        self.nextscanbtn.bind(on_release=self.on_next_scan)
        self.prevscanbtn = Button(text='<< Scan', size=BTNSIZE,
                                  size_hint=BTNHINT, font_size=FNTSIZE)
        self.prevscanbtn.bind(on_release=self.on_prev_scan)
        helpbtn = Button(text='Help', size=BTNSIZE, size_hint=BTNHINT,
                         font_size=FNTSIZE)
        helpbtn.bind(on_release=self.on_show_help)

        buttonlyt = BoxLayout(orientation='horizontal')
        buttonlyt.add_widget(self.annobtn)
        buttonlyt.add_widget(self.layerbtn)
        buttonlyt.add_widget(self.prevoctbtn)
        buttonlyt.add_widget(self.nextoctbtn)
        buttonlyt.add_widget(self.prevscanbtn)
        buttonlyt.add_widget(self.nextscanbtn)
        buttonlyt.add_widget(helpbtn)

        self.octnamelbl = Label(font_size=FNTSIZE)
        self.lockedlbl = Label(font_size=FNTSIZE, color=[1, 0, 0, 1])
        self.timerlbl = Label(pos=(dp(0), dp(10)), font_size=FNTSIZE)

        root = Widget()
        root.add_widget(self.octpanel)
        root.add_widget(self.octnamelbl)
        root.add_widget(self.lockedlbl)
        root.add_widget(self.timerlbl)
        root.add_widget(buttonlyt)

        self.prepare_annotation()
        self.load_annotation()
        self.show_first_oct()
        return root

    def prepare_annotation(self):
        """Create annotation file if it does not exist"""
        if osp.exists(self.annopath):
            return
        octpaths = glob(osp.join(self.datadir, '*' + OCTEXT))
        octids = [osp.splitext(osp.basename(p))[0] for p in octpaths]
        df = pd.DataFrame(octids, columns=[OCTID])
        df[DURATION] = None  # add empty duration column
        for name in LAYERS:  # add empty layer columns
            df[name] = None
        save_as_pickle(df, self.annopath)

    def resized(self, root, *args):
        """Window has been resized. Adjust label and button positions"""
        w, h = args
        self.octnamelbl.pos = (w / 2, h - 3 * BTNHEIGHT)
        self.lockedlbl.pos = (w / 2, h - 5 * BTNHEIGHT)

    def show_first_oct(self):
        """Display first scan of first OCT"""
        self.on_next_oct(None)
        self.prevoctbtn.disabled = True
        self.center_oct()

    def add_layer_btn(self, name):
        """Add button for layer with given name to dropdown menu"""
        btn = Button(text=name, size_hint_y=None, height=BTNHEIGHT,
                     font_size=FNTSMALLSIZE)
        btn.bind(on_release=self.on_select_layer)
        self.layerdd.add_widget(btn)
        self.layerbtn.disabled = False
        self.on_select_layer(btn)

    def update_layer_btns(self):
        """Update dropdown menu that shows layers"""
        layernames = [n.replace(PREFIX, '') for n in self.get_layernames()]
        self.layerdd.clear_widgets()
        for layername in layernames:
            self.add_layer_btn(layername)
        if not layernames:  # no layers
            self.layerdd.select(BTNLAYER)
            self.layerbtn.disabled = True

    def on_select_layer(self, btn):
        """Select layer button pressed"""
        self.layername = PREFIX + btn.text
        self.layerdd.select(btn.text)
        self.octpanel.display_scan()

    def center_oct(self):
        """Center OCT panel in main window"""
        ww, wh = Window.size
        _, sh, sw = self.oct.shape
        self.octpanel.pos = (ww - sw) / 2, (wh - sh) / 2

    def on_show_help(self, obj):
        """Show help button pressed"""
        text = Label(text=HELPTEXT, font_size=FNTSMALLSIZE)
        popup = Popup(title='Help', content=text,
                      size_hint=(None, None), size=POPHELPSIZE)
        popup.open()

    def update_status(self):
        """Update status text: OCT name and timer"""
        is_locked = "LOCKED" if self.scanidx in self.locked_scans else ""
        self.octnamelbl.text = '{}:{}'.format(self.oct_id, self.scanidx)
        self.lockedlbl.text = 'LOCKED' if is_locked else ''
        self.update_timer_status()

    def update_timer_status(self):
        durations = self.get_durations()
        if durations is None or durations != durations:  # None or NaN
            self.timerlbl.text = ''
            self.annotimer.reset_timing(do_callback=False, seconds=0)
        else:
            seconds = durations[self.scanidx]
            self.annotimer.reset_timing(do_callback=True, seconds=seconds)

    def update_time_display(self, seconds):
        """Update timer display with current time delta"""
        # set label to time difference in format HH:MM:SS
        tdelta = timedelta(seconds=seconds)
        self.timerlbl.text = str(tdelta).split('.')[0]

    def update_time_anno(self, seconds):
        """Update time annotation with duration in float seconds"""
        durations = self.get_durations()
        if durations is None:
            durations = [0.0 for _ in range(self.oct.shape[0])]
        durations[self.scanidx] = seconds
        self.df.at[self.dfindex[self.octidx], DURATION] = durations

    def get_durations(self):
        """Return annotation durations for current oct"""
        return self.get_cellvalue(self.octidx, DURATION)

    def get_cellvalue(self, octidx, column):
        """Return cell value from pandas table"""
        return self.df.loc[self.dfindex[octidx]][column]

    def get_layernames(self):
        return [n for n in self.df.columns.values if n.startswith(PREFIX)]

    def get_layeranno(self):
        """Return annotation for current layer or None"""
        if self.oct is None or self.layername is None:
            return None
        annos = self.get_cellvalue(self.octidx, self.layername)
        return annos[self.scanidx][1][0] if annos else None

    def get_layerannos(self):
        """Return annotation for all layer or empty list"""
        layerannos = []
        for layername in self.get_layernames():
            annos = self.get_cellvalue(self.octidx, layername)
            if annos and self.oct is not None:
                layerannos.append(annos[self.scanidx][1][0])
        return layerannos

    def update_layeranno(self):
        """Update layer annotation in pandas table"""

        def scananno():
            pointlist = []  # empty list of points
            return 'polyline', [pointlist]

        annos = self.get_cellvalue(self.octidx, self.layername)
        if annos is None:
            n = self.oct.shape[0]
            annos = tuple(scananno() for _ in range(n))
        self.df.at[self.dfindex[self.octidx], self.layername] = annos
        return annos[self.scanidx][1][0]  # pointlist

    def load_oct(self):
        """Loads the current OCT"""
        self.oct_id = self.get_cellvalue(self.octidx, OCTID)
        self.scanidx = 0
        self.prevscanbtn.disabled = True
        octpath = osp.join(self.datadir, self.oct_id + OCTEXT)
        cube = np.load(octpath)
        dtype = cube.dtype
        assert dtype == 'uint8', ('Expect cube data type to be uint8 but got ' +
                                  str(dtype))
        return cube

    def display_oct_scan(self):
        """Displays the current OCT scan"""
        self.octpanel.display_scan()
        self.update_status()

    def on_annotation(self, btn):
        """Annotation button pressed"""
        self.annodd.select(btn.text)
        if btn.text == BTNSAVE:
            self.save_annotation()
        elif btn.text == BTNRECOVER:
            self.recover()
        elif btn.text == BTNFILTER:
            self.filter_data_dialog()
        elif btn.text == BTNADDLAYER:
            self.add_layer_dialog()
        elif btn.text == BTNDELLAYER:
            self.del_layer_dialog()

    def filter_data_dialog(self):
        """Dialog for filtering pandas rows = OCTs"""
        filterin = TextInput(text='', multiline=False, font_size=FNTSIZE)

        def dismissed(_):
            query = filterin.text
            self.filter_table(query)
            print('select rows:', filterin.text)
            print('#rows selected:', len(self.dfindex))
            if not len(self.dfindex):
                self.filter_table('')
            self.show_first_oct()
            return False

        selectpu = Popup(title='Filter data',
                         size_hint=(None, None), size=POPSMALLSIZE)
        selectpu.add_widget(filterin)
        selectpu.bind(on_dismiss=dismissed)
        selectpu.open()

    def add_layer_dialog(self):
        """Dialog to add a new layer for annotation"""
        layerin = TextInput(text='', multiline=False, font_size=FNTSIZE)

        def dismissed(_):
            layername = layerin.text
            if layername:
                colname = PREFIX + layername
                self.df = self.df.assign(**{colname: lambda x: None})
                self.update_layer_btns()
            return False

        layerpu = Popup(title='Add layer annotation',
                        size_hint=(None, None), size=POPSMALLSIZE)
        layerpu.add_widget(layerin)
        layerpu.bind(on_dismiss=dismissed)
        layerpu.open()

    def del_layer_dialog(self):
        """Dialog to delete an existing annotation layer"""
        layerin = TextInput(text='', multiline=False, font_size=FNTSIZE)

        def dismissed(_):
            layername = layerin.text
            if layername:
                colname = PREFIX + layername
                self.df = self.df.drop(colname, axis=1)
                self.update_layer_btns()
            return False

        layerpu = Popup(title='Delete layer annotation',
                        size_hint=(None, None), size=POPSMALLSIZE)
        layerpu.add_widget(layerin)
        layerpu.bind(on_dismiss=dismissed)
        layerpu.open()

    def filter_table(self, query):
        """Filter pandas table with given query"""
        filtereddf = self.df.query(query, engine='python') if query else self.df
        self.dfindex = filtereddf.index.tolist()
        self.oct = None
        self.oct_id = ''
        self.octidx = -1
        self.scanidx = 0

    def recover(self):
        print('loading backup... ', self.backuppath, end='...')
        self.df = load_dataframe(self.backuppath)
        print('done.')
        self.filter_table(query='')
        self.update_layer_btns()
        self.show_first_oct()

    def load_annotation(self):
        """Load pandas table with annotation data"""
        print('loading annotation ...', self.annopath, end='...')
        self.df = load_dataframe(self.annopath)
        print('done.')
        # self.df.info()
        # print(self.df.head())
        self.filter_table(query='')
        self.update_layer_btns()

    def save_annotation(self):
        """Save annotation to pandas table"""
        if not self.df is None:
            print('saving annotation...', self.annopath, end='...')
            save_dataframe(self.df, self.annopath)
            print('done.')

    def save_backup(self):
        """Save annotation to backup pandas table"""
        if not self.df is None:
            print('saving backup... ', self.backuppath, end='...')
            save_dataframe(self.df, self.backuppath)
            print('done.')

    def on_next_oct(self, obj):
        """Next OCT button pressed"""
        n = len(self.dfindex) - 1
        self.annotimer.stop_timing()
        self.octidx += 0 if self.octidx >= n else 1
        self.nextoctbtn.disabled = self.octidx >= n
        self.prevoctbtn.disabled = False
        self.oct = self.load_oct()
        self.display_oct_scan()

    def on_prev_oct(self, obj):
        """Previous OCT button pressed"""
        self.annotimer.stop_timing()
        self.octidx -= 0 if self.octidx <= 0 else 1
        self.prevoctbtn.disabled = self.octidx <= 0
        self.nextoctbtn.disabled = False
        self.oct = self.load_oct()
        self.display_oct_scan()

    def on_prev_scan(self, obj):
        """Previous Scan button pressed"""
        self.annotimer.stop_timing()
        self.scanidx -= 0 if self.scanidx <= 0 else 1
        self.prevscanbtn.disabled = self.scanidx <= 0
        self.nextscanbtn.disabled = False
        self.display_oct_scan()

    def on_next_scan(self, obj):
        """Next Scan button pressed"""
        n = self.oct.shape[0] - 1
        self.annotimer.stop_timing()
        self.scanidx += 0 if self.scanidx >= n else 1
        self.nextscanbtn.disabled = self.scanidx >= n
        self.prevscanbtn.disabled = False
        self.display_oct_scan()

    def on_stop(self):
        """Stop application"""
        self.annotimer.event.set()  # stop timer
        if self.autosave:
            self.save_annotation()
        self.save_backup()
        return True

    def on_visible(self, btn):
        """Toggle visibility of layer annotation"""
        self.isvisible = not self.isvisible
        btn.text = BTNISVISIBLE[self.isvisible]
        self.octpanel.display_scan()

    def on_viewall(self, btn):
        """Toggle visibility of all layer annotations"""
        self.viewall = not self.viewall
        btn.text = BTNVIEWALL[self.viewall]
        self.octpanel.display_scan()

    def on_autosave(self, btn):
        """Toggle autosave"""
        self.autosave = not self.autosave
        btn.text = BTNAUTOSAVE[self.autosave]

    def key_down(self, key, scancode, codepoint, modifier, kwargs):
        """React on key press"""
        if scancode == KEYUP:
            self.prevoctbtn.trigger_action()
        elif scancode == KEYDOWN:
            self.nextoctbtn.trigger_action()
        elif scancode == KEYLEFT:
            self.prevscanbtn.trigger_action()
        elif scancode == KEYRIGHT:
            self.nextscanbtn.trigger_action()
        elif scancode == KEYLV:
            self.isvisblebtn.trigger_action()
        elif scancode == KEYLA:
            self.viewallbtn.trigger_action()
        elif scancode == KEYLS:
            self.annotimer.toggle_timing()
        elif scancode == KEYLR:
            self.annotimer.reset_timing()
        self.octpanel.editmode = EDITMODES.get(scancode, EDITOFF)

    def key_up(self, *wargs):
        """Keys released."""
        self.octpanel.editmode = EDITOFF
