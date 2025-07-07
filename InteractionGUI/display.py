import yaml
import PySimpleGUI as sg

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

"""
This file contains the class that contain functions for displaying features to user.
"""

# Constants:
MAX_TESTSTAND_NUM = 8
MAX_MODULE_NUM = 3

configuration = {}
with open('configuration.yaml', 'r') as file:
    configuration = yaml.safe_load(file)

class Display:
    def __init__(self):
        pass

    # ============================================================
    # === Windows Display ========================================
    # ============================================================

    def do_something_window(self, instruction: str, button: str, title=None, can_end=False):
        """
        Function which opens a window which tells the user to do something and has a button which is pressed once they've 
        done the thing. It has the option to allow the user to end the session instead of continuing, which when pressed
        makes the function return 'END'.
        """
        if title == None:
            title = instruction
        
        layout = [[sg.Text(instruction, font=lgfont)], [sg.Button(button)]]
        if can_end:
            layout[1].append(sg.Button("End Session"))
        window = sg.Window(f"Module Test: {instruction}", layout, margins=(200,100))

        ret = ''
        while True:
            event, values = window.read()
            if event == button or event == sg.WIN_CLOSED:
                ret = 'CONT'
                break
            if can_end and event == "End Session":
                ret = 'END'
                break
            
        window.close()
        return ret

    def waiting_window(self, message: str, title=None, description=None):
        """
        Function which opens a window when the GUI is handling something automatically and the user has to wait.
        """     
        if title is None:
            title = message

        layout = [[sg.Text(message, font=lgfont)]]
        if description is not None:
            layout.append([sg.Text(description)])
        window = sg.Window(f"Module Test: {message}", layout, margins=(200,100))

        event, values = window.read(timeout=100)
        return window

    def check_window(self, info: str):  # haven't test yet
        """
        Function which opens a window for user to check the input is correct or not.
        """
        # set up layout
        layout = [[sg.Text("Test Setup Check: ", font=lgfont)]]
        if info is not None:
            layout.append([sg.Text(info)])
        layout.append([[sg.Button("Return Last Step")], [sg.Button("Continue")]])

        # set up window
        window = sg.Window("Test Setup Check", layout, margins=(200,100))

        ret = ''    # initialize status

        # display
        while True:
            event, values = window.read()

            if event == "Return Last Step" or event == sg.WIN_CLOSED:
                break
            elif event == "Continue":
                ret = 'CONT'

        return ret


    # ============================================================
    # === Texts Display ==========================================
    # ============================================================

    def _setup_qr_code_input(self, teststand_no):
        """Set up layout for QR Code input
        """
        qr_code_input = []
        keys = []
        
        for module_no in range(MAX_MODULE_NUM):
            # set up keys
            key = f'-Scanned-QR-Code-{teststand_no}-{module_no}-'
            keys.append(key)

            # set up input area
            arg = sg.Input(s=20, key=key, enable_events=True)
            qr_code_input.append(arg)
        
        return qr_code_input, keys
    
    def _setup_teststand_buttons(self, teststand_no):
        """Set up buttons for 1 teststand.
        """
        buttons = [sg.Text('                         ')]
        keys = []

        for module_no in range(MAX_MODULE_NUM):
            # set up keys
            clear_key = f'-CLEAR-{teststand_no}-{module_no}-'
            manually_input_key = f'-ManualInput-{teststand_no}-{module_no}-'    # maybe we should replace it as moudle/hxb info
            keys.append(clear_key)
            keys.append(manually_input_key)

            # set up buttons
            buttons.append(sg.Button('Clear', key=clear_key))
            buttons.append(sg.Button('Manually Input', key=manually_input_key))
            buttons.append(sg.Text(''))

        return buttons, keys
    
    def _setup_teststand_ip(self, teststand_no):
        """Set up selection area for teststand ips.
        """
        key = f"-FPGAHostname-{teststand_no}-"
        arg = [sg.Text("Test Stand IP: "), 
               sg.Combo(configuration['FPGAHostname'], 
                    default_value=configuration['FPGAHostname'][(teststand_no-1)],  # `teststand_no` starts by 1
                    key=key)]
        
        return arg, [key]
    
    def _assign_layout(self, elements, is_vertical, MAX_COLUMNS):
        """Assign layout for given elements by given conditions.
        """
        layout = []

        if is_vertical:
            num_rows = (len(elements) + MAX_COLUMNS - 1) // MAX_COLUMNS
            for row in range(num_rows):
                this_row = []   # initialize the row

                for col in range(MAX_COLUMNS):
                    index = row + col * num_rows    # calculate the index of the current frame (column first)

                    if index < len(elements):  # avoid not-existing frame
                        this_row.append(elements[index])

                layout.append(this_row) 

        else:
            for i in range(0, len(elements), MAX_COLUMNS):
                layout.append(elements[i:i + MAX_COLUMNS])
        
        return layout

    def setup_single_teststand(self, teststand_no):
        """Set up single teststand layout.
        """
        qr_code_input, qr_code_input_keys = self._setup_qr_code_input(teststand_no)
        buttons, buttons_keys = self._setup_teststand_buttons(teststand_no)
        ip_arg, ip_key = self._setup_teststand_ip(teststand_no)

        single_teststand_keys = []

        # set up rows and teststand_setup
        row1 = [sg.Checkbox(f'Teststand {teststand_no}', key=f'-TESTSTAND-{teststand_no}-', enable_events=True, default = False)] + qr_code_input
        row2 = buttons
        row3 = [sg.Text('  ')] + ip_arg

        teststand_setup = [row1, row2, row3]

        # set up keys
        single_teststand_keys.extend(qr_code_input_keys)
        single_teststand_keys.extend(buttons_keys)
        single_teststand_keys.extend(ip_key)

        return sg.Frame('', teststand_setup), single_teststand_keys
    
    def setup_all_teststands(self, is_vertical=True, MAX_COLUMNS=2):
        """Set up the teststands layout.
        """
        all_teststands_setup = []
        all_teststands_keys = []
        single_frames = []

        for teststand_no in range(1, MAX_TESTSTAND_NUM+1):
            single_teststand_setup, single_teststand_keys = self.setup_single_teststand(teststand_no)

            all_teststands_keys.extend(single_teststand_keys)
            single_frames.append(single_teststand_setup)
        
        all_teststands_setup = self._assign_layout(single_frames, is_vertical, MAX_COLUMNS)

        return sg.Frame('TestStands Setup', layout=all_teststands_setup, key='-TESTSTAND-FRAME-', visible=True), all_teststands_keys
    

    # ============================================================
    # === LEDs Display ===========================================
    # ============================================================

    # Functions for current state status indicators
    def LEDIndicator(self, key=None, radius=30):
        return sg.Graph(canvas_size=(radius, radius),
                        graph_bottom_left=(-radius, -radius),
                        graph_top_right=(radius, radius),
                        pad=(0, 0), key=key, visible=True)
    
    def SetLED(window, key, color, empty=False):
        graph = window[key]
        graph.erase()
        if not empty:
            graph.draw_circle((0, 0), 12, fill_color=color, line_color=color)
        else:
            graph.draw_circle((0, 0), 12, fill_color=None, line_color=color)
    
    # ============================================================
    # === status bar Display ===========================================
    # ============================================================

    def statusbar(self):
        """ This function sets up the statusbar.
        """

        STATUS_SBCOL1 = sg.Frame('', [[sg.Text("Debug Mode: "), sg.Push(), self.LEDIndicator(key='-Debug-Mode-')],
                            [sg.Text("Is Live Module: "), sg.Push(), self.LEDIndicator(key='-Live-Module-')],
                            [sg.Text("HV Cable Connected: "), sg.Push(), self.LEDIndicator(key='-HV-Connected-')]],key = "-status_sbcol1-frame-")
        STATUS_SBCOL2 = sg.Frame('', [[sg.Text("Dark Box Closed: "), sg.Push(), self.LEDIndicator(key='-Box-Closed-')],
                            [sg.Text("HV Output Powered: "), sg.Push(), self.LEDIndicator(key='-HV-Output-On-')],
                            [sg.Text("DCDC Connected: ", key='-DCDC-Connected-Txt-'), sg.Push(), self.LEDIndicator(key='-DCDC-Connected-')]],key = "-status_sbcol2-frame-")
        STATUS_SBCOL3 = sg.Frame('', [[sg.Text("DCDC Powered: ", key='-DCDC-Powered-Txt-'), sg.Push(), self.LEDIndicator(key='-DCDC-Powered-')],
                            [sg.Text("Trophy Connected: "), sg.Push(), self.LEDIndicator(key='-Trophy-Connected-')],
                            [sg.Text("Hexacontroller Connected: "), sg.Push(), self.LEDIndicator(key='-Hexactrl-Connected-')]],key = "-status_sbcol3-frame-")
        STATUS_SBCOL4 = sg.Frame('', [[sg.Text("Hexacontroller Powered: "), sg.Push(), self.LEDIndicator(key='-Hexactrl-Powered-')],
                            [sg.Text("Hexacontroller Accessed: "), sg.Push(), self.LEDIndicator(key='-Hexactrl-Accessed-')],
                            [sg.Text("Firmware Loaded: "), sg.Push(), self.LEDIndicator(key='-FW-Loaded-')]],key = "-status_sbcol4-frame-")
        STATUS_SBCOL5 = sg.Frame('', [[sg.Text("DAQ Server: "), sg.Push(), self.LEDIndicator(key='-DAQ-Server-')],
                            [sg.Text("I2C Server: "), sg.Push(), self.LEDIndicator(key='-I2C-Server-')],
                            [sg.Text("DAQ Client: "), sg.Push(), self.LEDIndicator(key='-DAQ-Client-')]],key = "-status_sbcol5-frame-")
        
        return [[STATUS_SBCOL1, STATUS_SBCOL2, STATUS_SBCOL3, STATUS_SBCOL4, STATUS_SBCOL5]]