import sys
import PySimpleGUI as sg
from time import sleep, time
from InteractionGUI import Display
from datetime import datetime, timedelta

import yaml

"""
This script stores all the layout information.
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

# Inspectors
INSPECTOR = display_obj.setup_inspectors()


#GUI LAYOUT
GUI_LAYOUT = [[sg.Text("Module Testing GUI", font=lgfont, text_color=cmured)], 
               LOGO + INSPECTOR,
              [TESTSTANDS],
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

