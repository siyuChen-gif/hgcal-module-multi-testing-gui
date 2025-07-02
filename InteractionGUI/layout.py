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

display_obj = display.display()

# Create theme

LGFONT = ('Arial', 2*int(configuration['DefaultFontSize']))

CMURED = '#C41230'
BKGGRAY = '#252525'
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
STATUS_SBCOL1 = sg.Frame('', [[sg.Text("Debug Mode: "), sg.Push(), display_obj.LEDIndicator(key='-Debug-Mode-')],
                       [sg.Text("Is Live Module: "), sg.Push(), display_obj.LEDIndicator(key='-Live-Module-')],
                       [sg.Text("HV Cable Connected: "), sg.Push(), display_obj.LEDIndicator(key='-HV-Connected-')]])
STATUS_SBCOL2 = sg.Frame('', [[sg.Text("Dark Box Closed: "), sg.Push(), display_obj.LEDIndicator(key='-Box-Closed-')],
                       [sg.Text("HV Output Powered: "), sg.Push(), display_obj.LEDIndicator(key='-HV-Output-On-')],
                       [sg.Text("DCDC Connected: ", key='-DCDC-Connected-Txt-'), sg.Push(), display_obj.LEDIndicator(key='-DCDC-Connected-')]])
STATUS_SBCOL3 = sg.Frame('', [[sg.Text("DCDC Powered: ", key='-DCDC-Powered-Txt-'), sg.Push(), display_obj.LEDIndicator(key='-DCDC-Powered-')],
                       [sg.Text("Trophy Connected: "), sg.Push(), display_obj.LEDIndicator(key='-Trophy-Connected-')],
                       [sg.Text("Hexacontroller Connected: "), sg.Push(), display_obj.LEDIndicator(key='-Hexactrl-Connected-')]])
STATUS_SBCOL4 = sg.Frame('', [[sg.Text("Hexacontroller Powered: "), sg.Push(), display_obj.LEDIndicator(key='-Hexactrl-Powered-')],
                       [sg.Text("Hexacontroller Accessed: "), sg.Push(), display_obj.LEDIndicator(key='-Hexactrl-Accessed-')],
                       [sg.Text("Firmware Loaded: "), sg.Push(), display_obj.LEDIndicator(key='-FW-Loaded-')]])
STATUS_SBCOL5 = sg.Frame('', [[sg.Text("DAQ Server: "), sg.Push(), display_obj.LEDIndicator(key='-DAQ-Server-')],
                       [sg.Text("I2C Server: "), sg.Push(), display_obj.LEDIndicator(key='-I2C-Server-')],
                       [sg.Text("DAQ Client: "), sg.Push(), display_obj.LEDIndicator(key='-DAQ-Client-')]])

STATUSBAR= [[STATUS_SBCOL1, STATUS_SBCOL2, STATUS_SBCOL3, STATUS_SBCOL4, STATUS_SBCOL5]]

#GUI LAYOUT
GUI_LAYOUT = [[sg.Text("Module Testing GUI", font=LGFONT, text_color=CMURED)], logo,
          [sg.Push(), sg.Button("Grade Module")],
          [sg.Text(key='-EXPAND-', font='ANY 1', pad=(0, 0))],
          [sg.Frame('Status Bar', STATUSBAR)]]



# layout for status
# Set the initial colors and values of the status indicators
ledlist = ['-Debug-Mode-', '-Live-Module-', '-HV-Connected-', '-Box-Closed-', '-HV-Output-On-', '-DCDC-Connected-', '-DCDC-Powered-', '-Trophy-Connected-',
           '-Hexactrl-Connected-', '-Hexactrl-Powered-', '-Hexactrl-Accessed-', '-FW-Loaded-', '-DAQ-Server-', '-I2C-Server-', '-DAQ-Client-' ]

