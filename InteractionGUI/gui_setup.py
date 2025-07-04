import PySimpleGUI as sg
from InteractionGUI.display import Display, MAX_TESTSTAND_NUM
from InteractionGUI.state_controller import StateController

class SetUpGUI:
    """
    This class contains all the functions that will be auto used to set up the BaseGUI window.
    """
    def __init__(self, window):
        self.window = window

        self.display = Display()
        self.state = StateController(self.window)

    # ============================================================
    # === Interactions  ==========================================
    # ============================================================

    """ Functions for enabling/disabling teststand setup fields. """
    def enable_all_teststands(self):
        _, keys = self.display.setup_all_teststands()
        for key in keys:
            self.state.enable(key)
    def disable_all_teststands(self):
        _, keys = self.display.setup_all_teststands()
        for key in keys:
            self.state.disable(key)
    
    """ Functions for enabling/disabling one teststand setup fields. """
    def enable_one_teststand(self, teststand_no):
        _, keys = self.display.setup_single_teststand(teststand_no)
        for key in keys:
            self.state.enable(key)
    def disable_one_teststand(self, teststand_no):
        _, keys = self.display.setup_single_teststand(teststand_no)
        for key in keys:
            self.state.disable(key)

    """ Functions for checking/unchecking teststand checkboxs """
    def check_all_teststands_checkboxs(self):
        for teststand_no in range(1, MAX_TESTSTAND_NUM + 1):
            key = f'-TESTSTAND-{teststand_no}-'
            self.state.update_value(key, True)
    def uncheck_all_teststands_checkboxs(self):
        for teststand_no in range(1, MAX_TESTSTAND_NUM + 1):
            key = f'-TESTSTAND-{teststand_no}-'
            self.state.update_value(key, False)

    """ Functions for clear the Scan QR Code input """
    def clear_scanned_qr_code(self, key):
        self.state.update_value(key, '')
    
    """ Function for displaying/hiding the entire Teststand Setup section """
    def show_teststands_setup(self):
        self.state.set_visibility('-TESTSTAND-FRAME-', True)
    def hide_teststands_setup(self):
        self.state.set_visibility('-TESTSTAND-FRAME-', False)