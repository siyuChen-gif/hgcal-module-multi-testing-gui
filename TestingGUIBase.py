import sys
import PySimpleGUI as sg
from Keithley2410 import Keithley2410
from time import sleep, time
from InteractionGUI import *
from datetime import datetime, timedelta

from InteractionGUI import layout
from DBTools import add_RH_T, readout_info, iv_info, assembly_info, summary_upload, fetch_comments, serial_remove_dashes

"""
This script creates and runs the main GUI window for the testing system. It firsts establishes a theme and sets some functions, 
then creates the GUI layout and then the GUI window. Once done, the script runs a loop which tracks and responds to the user's
interaction with the layout.
"""


"""
   Create Window
"""

sg.LOOK_AND_FEEL_TABLE['cmutheme'] = layout.CMUTHEME
sg.theme('cmutheme')

basewindow = sg.Window("Module Test: Start", layout.GUI_LAYOUT, margins=(200,80), finalize=True, resizable=True, return_keyboard_events=True)
# margins can be changed to suit the monitor; these are for a 1080p monitor
basewindow['-EXPAND-'].expand(True, True, True) # expand space between menus and status bar
event, values = basewindow.read(timeout=10)
basewindow.maximize()

for led in layout.ledlist:
    SetLED(basewindow, led, 'black', empty=True)
SetLED(basewindow, '-Debug-Mode-', 'green' if DEBUG_MODE else 'red')