import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import yaml
import PySimpleGUI as sg
from InteractionGUI import Display, GUISetUp, GUIEventHandler

configuration = {}
with open('../configuration.yaml', 'r') as file:
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
display = Display()

# Initialize the basewindow
teststand_display, _ = display.setup_all_teststands()

layout = [[teststand_display],
          [sg.Button("Enable ALL"), 
           sg.Button("Disable ALL"),
           sg.Button("Display ALL"),
           sg.Button("Hide ALL"),
           sg.Push(),
           sg.Button("Exit")]]

basewindow = sg.Window("Test Teststand Display", layout, resizable=True, finalize=True)
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