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

configuration = {}
with open('./configuration.yaml', 'r') as file:
    configuration = yaml.safe_load(file)

# Create theme
lgfont = ('Arial', 2*int(configuration['DefaultFontSize']))
sg.set_options(font=("Arial", int(configuration['DefaultFontSize'])))

cmured = '#C41230'
bkggray = '#252525'
cmutheme = {'BACKGROUND': bkggray,
            'TEXT': '#FFFFFF', 
            'INPUT': bkggray,
            'TEXT_INPUT': '#FFFFFF',
            'SCROLL': cmured,
            'BUTTON': (cmured, bkggray),
            'PROGRESS': ('#000000', '#000000'),
            'BORDER': 1,
            'SLIDER_DEPTH': 0,
            'PROGRESS_DEPTH': 0,
            'COLOR_LIST': [cmured, '#FFFFFF', bkggray],
            'DESCRIPTION': ['Red', 'Blue', 'Grey', 'Vintage', 'Wedding']}
sg.LOOK_AND_FEEL_TABLE['cmutheme'] = cmutheme
sg.theme('cmutheme')

# Initialize the class
display_obj = Display()

#logo
vers0 = sys.version_info[0]
vers1 = sys.version_info[1]
if vers0 == 3 and vers1 >= 9:
    LOGO = [sg.Image('hexmap/geometries/cmu-wordmark-horizontal-r-resized.png')]
elif vers0 == 3 and vers1 < 9:
    LOGO = [sg.Text("Carnegie Mellon University", text_color=cmured, font=('Arial', 20))]

# Status bar
STATUSBAR = display_obj.statusbar()

# Test stand
TESTSTANDS, _ = display_obj.setup_all_teststands()


#GUI LAYOUT
GUI_LAYOUT = [[sg.Text("Module Testing GUI", font=lgfont, text_color=cmured)], LOGO,
              [sg.Push(), TESTSTANDS, sg.Push()],
              [sg.Button("Enable ALL"), 
               sg.Button("Disable ALL"),
               sg.Button("Display ALL"),
               sg.Button("Hide ALL"),
               sg.Push(),
               sg.Button("Exit")],
              [sg.Text(key='-EXPAND-', font='ANY 1', pad=(0, 0))],
              [sg.Frame("STATUS",STATUSBAR, key="-statusbar_frame-")]]


# layout for status
# Set the initial colors and values of the status indicators
ledlist = ['-Debug-Mode-', '-Live-Module-', '-HV-Connected-', '-Box-Closed-', '-HV-Output-On-', '-DCDC-Connected-', '-DCDC-Powered-', '-Trophy-Connected-',
           '-Hexactrl-Connected-', '-Hexactrl-Powered-', '-Hexactrl-Accessed-', '-FW-Loaded-', '-DAQ-Server-', '-I2C-Server-', '-DAQ-Client-' ]


basewindow = sg.Window("Module Test: Start", GUI_LAYOUT, margins=(100,80), finalize=True, resizable=True, return_keyboard_events=True)
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