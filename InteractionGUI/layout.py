import sys
import PySimpleGUI as sg
from time import sleep, time
from InteractionGUI import display
from datetime import datetime, timedelta

import yaml

"""
This script stores all the layout information.
"""

# Load configuration file
configuration = {}
with open('configuration.yaml', 'r') as file:
    configuration = yaml.safe_load(file)

display_obj = display.Display()

# Create theme

LGFONT = ('Arial', 2*int(configuration['DefaultFontSize']))
sg.set_options(font=("Arial", int(configuration['DefaultFontSize'])))

CMURED = '#C41230'
BKGGRAY = "#252525"
CMUTHEME = {'BACKGROUND': BKGGRAY,
            'TEXT': '#FFFFFF', 
            'INPUT': BKGGRAY,
            'TEXT_INPUT': '#FFFFFF',
            'SCROLL': CMURED,
            'BUTTON': (CMURED, BKGGRAY),
            'PROGRESS': ('#000000', '#000000'),
            'BORDER': 1,
            'SLIDER_DEPTH': 0,
            'PROGRESS_DEPTH': 0,
            'COLOR_LIST': [CMURED, '#FFFFFF', BKGGRAY],
            'DESCRIPTION': ['Red', 'Blue', 'Grey', 'Vintage', 'Wedding']}

#logo
vers0 = sys.version_info[0]
vers1 = sys.version_info[1]
if vers0 == 3 and vers1 >= 9:
    LOGO = [sg.Image('hexmap/geometries/cmu-wordmark-horizontal-r-resized.png')]
elif vers0 == 3 and vers1 < 9:
    LOGO = [sg.Text("Carnegie Mellon University", text_color=CMURED, font=('Arial', 20))]

# Status bar
STATUSBAR = display_obj.statusbar()

# Test stand
TESTSTANDS, _ = display_obj.setup_all_teststands()


#GUI LAYOUT
GUI_LAYOUT = [[sg.Text("Module Testing GUI", font=LGFONT, text_color=CMURED)], LOGO,
            [TESTSTANDS],
          [sg.Button("Enable ALL"), 
           sg.Button("Disable ALL"),
           sg.Button("Display ALL"),
           sg.Button("Hide ALL"),
           sg.Push(),
           sg.Button("Exit")],
           [sg.Text(key='-EXPAND-', font='ANY 1', pad=(0, 0))],
           STATUSBAR]


# layout for status
# Set the initial colors and values of the status indicators
ledlist = ['-Debug-Mode-', '-Live-Module-', '-HV-Connected-', '-Box-Closed-', '-HV-Output-On-', '-DCDC-Connected-', '-DCDC-Powered-', '-Trophy-Connected-',
           '-Hexactrl-Connected-', '-Hexactrl-Powered-', '-Hexactrl-Accessed-', '-FW-Loaded-', '-DAQ-Server-', '-I2C-Server-', '-DAQ-Client-' ]

