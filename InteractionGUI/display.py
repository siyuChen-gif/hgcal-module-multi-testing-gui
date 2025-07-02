

class Display:
    """
    This class contains functions for displaying features to user.
    """

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

    # Devoloping
    def check_window(self):
        """
        Function which opens a window for user to check the test setup.
        """
        return window


    # ============================================================
    # === Texts Display ==========================================
    # ============================================================

    # Developing
    def single_teststand_display(self, teststand_no: int):
        """Set up a teststand layout.
        """
        return 
    
    def setup_teststands(self, visible=True):
        """Set up the teststands layout -> 8 teststands in total.
        """
        return
    
    
    # ============================================================
    # === Buttons Display ========================================
    # ============================================================

    # Developing
    def SetLED(self, color: str);
        """This is the button for reading information from the status.
        """
        button = sg.Button()
        retunr button
    
