import yaml
import PySimpleGUI as sg
from InteractionGUI.display import Display
from InteractionGUI.interaction import HumanInteraction
from InteractionGUI.handle_process import SetUpGUI

configuration = {}
with open('configuration.yaml', 'r') as file:
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
setup = SetUpGUI()
human_interact = HumanInteraction()


# Initialize the basewindow
teststand_display, _ = display.setup_all_teststands()

layout = [[teststand_display],
          [sg.Button("Enable ALL"), sg.Button("Disable ALL")],
          [sg.Button("Exit")]]

basewindow = sg.Window("Test Teststand Display", layout, resizable=True, finalize=True)
setup.disable_all_teststands_setup(basewindow)


# start the event loop
while True:
    event, values = basewindow.read()
    if event == sg.WINDOW_CLOSED or event == "Exit":
        break
    elif event == "Enable ALL":
        human_interact.enable_all_teststands_setup(basewindow)
        setup.check_all_teststands_checkboxs(basewindow)
    elif event == "Disable ALL":
        human_interact.disable_all_teststands_setup(basewindow)
        setup.uncheck_all_teststands_checkboxs(basewindow)
    elif event.startswith('-TESTSTAND-'):
        ts_id = int(event.split('-')[2])
        is_checked = values[event]
        if is_checked:
            human_interact.enable_one_teststand_setup(basewindow, ts_id)
        else:
            human_interact.disable_one_teststand_setup(basewindow, ts_id)

basewindow.close()