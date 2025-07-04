from InteractionGUI.gui_setup import SetUpGUI

class GUIEventHandler:
    """
    This class contains all the functions that will be auto used to handle the events of the BaseGUI window.
    """
    def __init__(self, window):
        self.setup = SetUpGUI(window)
        # The below function map is used to map the event name that does not have any patterns to the corresponding handler function.
        self.event_map = {
            "Enable ALL": self.handle_enable_all,
            "Disable ALL": self.handle_disable_all,
            "Display ALL": self.handle_display_all,
            "Hide ALL": self.handle_hide_all,
        }

    # ============================================================
    # === API  ===================================================
    # ============================================================

    def handle_event(self, event, values):
        """This is the API for this entire class. 
           - User will only need to call this function to handle all the events from the BaseGUI window.
        """
        if event in self.event_map:
            self.event_map[event]()  # call handler
            return

        # Pattern matching
        if event.startswith('-TESTSTAND-'):
            self.handle_teststand_checkbox(event, values)

        elif event.startswith('-CLEAR-'):
            self.handle_clear(event)

        """ More elifs here for future cases... """
    

    # ============================================================
    # === Handler Implementations  ===============================
    # ============================================================

    def handle_enable_all(self):
        self.setup.enable_all_teststands()
        self.setup.check_all_teststands_checkboxs()

    def handle_disable_all(self):
        self.setup.disable_all_teststands()
        self.setup.uncheck_all_teststands_checkboxs()

    def handle_display_all(self):
        self.setup.show_teststands_setup()

    def handle_hide_all(self):
        self.setup.hide_teststands_setup()

    def handle_teststand_checkbox(self, event, values):
        """
        checkbox key: '-TESTSTAND-{teststand_no}-'
        """
        ts_no = int(event.split('-')[2])
        is_checked = values[event]
        if is_checked:
            self.setup.enable_one_teststand(ts_no)
        else:
            self.setup.disable_one_teststand(ts_no)

    def handle_clear(self, event):
        """
        clear button key:   '-CLEAR-{teststand_no}-{module_no}-'
        input box key:      '-Scanned-QR-Code-{teststand_no}-{module_no}-'
        """
        ts_no     = int(event.split('-')[2])
        module_no = int(event.split('-')[3])
        key       = f"-Scanned-QR-Code-{ts_no}-{module_no}-"
        self.setup.clear_scanned_qr_code(key)