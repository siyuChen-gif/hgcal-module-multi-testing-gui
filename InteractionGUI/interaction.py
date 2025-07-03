import PySimpleGUI as sg
from InteractionGUI.display import Display

class HumanInteraction:
    """This class contains all the functions that would be activate when user interact with the GUI
    """
    def __init__(self):
        self.display = Display()

    # Functions for enabling/disabling teststand setup fields
    def toggle_all_teststands_setup(self, window, enabled):
        _, keys = self.display.setup_all_teststands()
        for key in keys:
            window[key].update(disabled=(not enabled))
    
    def enable_all_teststands_setup(self, window):
        self.toggle_all_teststands_setup(window, True)
    def disable_all_teststands_setup(self, window):
        self.toggle_all_teststands_setup(window, False)
    
    # Functions for enabling/disabling one teststand setup fields
    def toggle_one_teststand_setup(self, window, teststand_no, enable):
        _, keys = self.display.setup_single_teststand(teststand_no)
        for key in keys:
            window[key].update(disabled=(not enable))
    
    def enable_one_teststand_setup(self, window, teststand_no):
        self.toggle_one_teststand_setup(window, teststand_no, True)
    def disable_one_teststand_setup(self, window, teststand_no):
       self.toggle_one_teststand_setup(window, teststand_no, False)
