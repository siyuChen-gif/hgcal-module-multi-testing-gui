import PySimpleGUI as sg
import yaml

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

    def do_something_window(instruction: str, button: str, title=None, can_end=False):
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

    def waiting_window(message: str, title=None, description=None):
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

    def check_window(self, info: str):
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

            if event == "Return Last Step":
                ret = 'TERM'
            elif event == "Continue" or event == sg.WIN_CLOSED:
                ret = 'CONT'

        return ret


    # ============================================================
    # === Texts Display ==========================================
    # ============================================================

    def setup_qr_code_input(self, teststand_no: int) -> list:
        """Set up layout for QR Code input
        """
        qr_code_input = []
        
        for module_no in range(MAX_MODULE_NUM):
            arg = sg.Input(s=20, key=f'-Scanned-QR-Code-{teststand_no}-{module_no}-', enable_events=True)
            qr_code_input.append(arg)
        
        return qr_code_input
    
    def setup_teststand_buttons(self, teststand_no: int) -> list:
        """Set up buttons for 1 teststand.
        """
        buttons = []
        for module_no in range(MAX_MODULE_NUM):
            buttons.append(sg.Button('Clear', key=f'-CLEAR-{teststand_no}-{module_no}-'))
            buttons.append(sg.Button('Manual Input', key=f'-ManualInput-{teststand_no}-{module_no}-'))
        return buttons

    def setup_single_teststand(self, teststand_no: int):
        """Set up single teststand layout.
        """
        qr_code_input = self.setup_qr_code_input(teststand_no)
        buttons = self.setup_teststand_buttons(teststand_no)

        # set up rows
        row1 = [sg.Checkbox(f'Teststand {teststand_no}', key=f'-TESTSTAND-{teststand_no}-', enable_events=True, default = False)] + qr_code_input
        row2 = [sg.Text("Test Stand IP: "), 
                sg.Combo(configuration['FPGAHostname'], 
                    default_value=configuration['FPGAHostname'][(teststand_no)], 
                    key=f"-FPGAHostname-{teststand_no}-")]+ buttons

        teststand_setup = [row1, row2]

        return sg.Frame('', teststand_setup)
    
    def setup_all_teststands(self, visible=True):
        """Set up the teststands layout.
        """
        all_teststands = []

        for teststand_no in range(MAX_TESTSTAND_NUM):
            single_teststand = self.setup_single_teststand(teststand_no)
            all_teststands.append([single_teststand])

        return sg.Frame('TestStands Setup', layout=all_teststands, visible=visible)
    
    
    # ============================================================
    # === Buttons Display ========================================
    # ============================================================

    # Functions for current state status indicators
    def LEDIndicator(key=None, radius=30):
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
