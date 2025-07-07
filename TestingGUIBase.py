import sys
import PySimpleGUI as sg
import os
from time import sleep, time
from datetime import datetime, timedelta
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import yaml

from InteractionGUI import layout, Display, GUISetUp, GUIEventHandler
from DBTools import add_RH_T, readout_info, iv_info, assembly_info, summary_upload, fetch_comments, serial_remove_dashes
from Keithley2410 import Keithley2410

"""
This script creates and runs the main GUI window for the testing system. It firsts establishes a theme and sets some functions, 
then creates the GUI layout and then the GUI window. Once done, the script runs a loop which tracks and responds to the user's
interaction with the layout.
"""


"""
   Create Window
"""

basewindow = sg.Window("Module Test: Start", layout.GUI_LAYOUT, margins=(100,80), finalize=True, resizable=True, return_keyboard_events=True)
# # margins can be changed to suit the monitor; these are for a 1080p monitor

# expand objects
basewindow['-EXPAND-'].expand(True, True, True) # expand space between menus and status bar
basewindow.maximize()

# Initialize the event handler
setup = GUISetUp(basewindow)
handler = GUIEventHandler(basewindow)

# Disable all teststands by default
setup.disable_all_teststands()

# start the event loop
while True:
    event, values = basewindow.read()

    if event == sg.WINDOW_CLOSED or event == "Exit":
        break

    handler.handle_event(event, values)


basewindow.close()