from InteractionGUI.setup import GUISetUp

class GUIEventHandler:
    """
    This class contains all the functions that will be auto used to handle the events of the BaseGUI window.
    """
    def __init__(self, window):
        self.setup = GUISetUp(window)
        # The below function map is used to map the event name that does not have any patterns to the corresponding handler function.
        self.event_map = {
            "Enable ALL": self.handle_enable_all,
            "Disable ALL": self.handle_disable_all,
            "Display ALL": self.handle_display_all,
            "Hide ALL": self.handle_hide_all,
        }
        # The above event map is currently for demonstration purposes only.

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

        """ More elifs here for future usage... """
    

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
        teststand_no, _ = self._get_no_from_event(event)
        is_checked = values.get(event, False)

        if is_checked:
            self.setup.enable_one_teststand(teststand_no)
        else:
            self.setup.disable_one_teststand(teststand_no)

    def handle_clear(self, event):
        """
        clear button key:   '-CLEAR-{teststand_no}-{module_no}-'
        input box key:      '-Scanned-QR-Code-{teststand_no}-{module_no}-'
        """
        teststand_no, module_no = self._get_no_from_event(event)
        key       = f"-Scanned-QR-Code-{teststand_no}-{module_no}-"

        self.setup.clear_scanned_qr_code(key)


    # ============================================================
    # === Helper Functions  ======================================
    # ============================================================

    def _get_no_from_event(self, event):
        """Helper function to extract the teststand and module number from the event key.
        """
        parts = event.strip('-').split('-')
        nums = [int(p) for p in parts if p.isdigit()]   # filter out the digit

        # assert the first number is the teststand number
        teststand_no = nums[0]

        if len(nums) == 2:
            module_no = nums[1]
        else:
            module_no = None
        
        return teststand_no, module_no