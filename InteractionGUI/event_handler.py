from time import sleep
import PySimpleGUI as sg

from InteractionGUI.setup import GUISetUp
from InteractionGUI.display import Display
from InteractionGUI.value_handler import GUIValueHandler
from InteractionGUI.status_handler import GUIStatusModel

# Constants:
MAX_TESTSTAND_NUM = 8
MAX_MODULE_NUM = 3
DEBUG_MODE = True

class GUIEventHandler:
    """
    This class contains all the functions that will be auto used to handle the events of the BaseGUI window.
    """
    def __init__(self, window):
        self.setup = GUISetUp(window)
        self.value_handler = GUIValueHandler(window)
        self.display = Display()
        self.status = GUIStatusModel(window)

        # The below function map is used to map the event name that does not have any patterns to the corresponding handler function.
        self.event_map = {
            "Select ALL": self.handle_enable_all,
            "De-Select ALL": self.handle_disable_all,
            "-Configure-Test-Stand-": self.handle_configure_teststand,
            "-Back-To-Base": self.handle_back_to_base,
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
        
        elif event.startswith('-Scanned-QR-Code-'):
            self.handle_module_status_combo(event, values)
        
        elif event.startswith('-TestSelectionButton-'):
            self.handle_popup_test_selection(event, values)

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
        checkbox key:           '-TESTSTAND-{teststand_no}-'
        selected status key:    'is_selected'
        """
        teststand_no, _ = self._get_no_from_event(event)
        is_checked = values.get(event, False)

        if is_checked:
            self.setup.enable_one_teststand(teststand_no)
            self.status.update_status("is_selected", teststand_no)

            fpgahostname = self.value_handler.get_fpgahostname(teststand_no)
            self.status.update_value("fpgahostname", teststand_no, value=fpgahostname)
            
        else:
            self.setup.disable_one_teststand(teststand_no)
            self.status.update_status("is_selected", teststand_no, value=False)
            self.status.update_value("fpgahostname", teststand_no)

    def handle_clear(self, event):
        """
        clear button key:           '-CLEAR-{teststand_no}-{module_no}-'
        input box key:              '-Scanned-QR-Code-{teststand_no}-{module_no}-'
        module status combo key:    '-ModuleStatus-{teststand_no}-{module_no}-' 
        """
        teststand_no, module_no = self._get_no_from_event(event)
        key       = f"-Scanned-QR-Code-{teststand_no}-{module_no}-"
        combo_key = f'-ModuleStatus-{teststand_no}-{module_no}-'

        self.setup.clear_scanned_qr_code(key)
        self.setup.update_combo(combo_key, [])
    
    def handle_module_status_combo(self, event, values):
        """
        scanned QR code key:        '-Scanned-QR-Code-{teststand_no}-{module_no}-'   
        module status combo key:    '-ModuleStatus-{teststand_no}-{module_no}-'
        """
        teststand_no, module_no = self._get_no_from_event(event)
        combo_key = f'-ModuleStatus-{teststand_no}-{module_no}-'
        qr_key = f'-Scanned-QR-Code-{teststand_no}-{module_no}-'

        scanned_qr_code = values.get(qr_key, '')
        moduleserial = self.value_handler.format_moduleserial(scanned_qr_code)

        valid_state = self.value_handler.check_valid_module_serial(moduleserial)
        if valid_state == 'invalid':
            valid = False
        else:
            valid = True

        is_live = self.value_handler.check_is_live(moduleserial)
        is_hxb = self.value_handler.check_is_hxb(moduleserial)

        if is_live and valid:
            mod_statuses = ['Assembled', 'Backside Bonded', 'Backside Encapsulated',
                            'Completely Bonded', 'Bonds Reworked', 'Completely Encapsulated', 'Bolted']
            self.setup.update_combo(combo_key, mod_statuses)
        elif is_hxb and valid:
            hxb_statuses = ['Untaped', 'Taped']
            self.setup.update_combo(combo_key, hxb_statuses)
        else:
            self.setup.update_combo(combo_key, [])
        
    def handle_configure_teststand(self):
        """
        configure teststand button key: '-Configure-Test-Stand-'
        """
        self.setup.disable_key("-Configure-Test-Stand-")

        configured = True   # assert all teststands configured

        if DEBUG_MODE:
            sleep(1)
        
        if configured:
            self._update_temp_value_map()

            temp_value_maps = self.status.temp_value_maps

            end = self.display.waiting_window("Test stands configured.")
            sleep(1)
            end.close()
            
            # hide the configuration setup frame
            self.setup.hide_teststands_setup()

            # display the testselection frame
            self.setup.delete_tests_selection_setup()   # remove the placeholder

            TEST_SETUP_LAYOUT = self.display.setup_all_test_selection(temp_value_maps)
            
            # add the test selection frame to the window
            self.setup.add_tests_selection_setup(TEST_SETUP_LAYOUT)

            # show the frame
            self.setup.show_tests_selection_setup()

            # update the default test
            self._update_default_test(temp_value_maps)

            # enable the configuration setup button for future usage -> re-configure test stands
            self.setup.enable_key("-Configure-Test-Stand-")
        
    def handle_popup_test_selection(self, event, values):
        """
        test selection key:        "-TestSelection-{teststand_no}-{module_no}-"
        test selection button key: "-TestSelectionButton-{teststand_no}-{module_no}-"
        """
        # get the teststand and module number from the event key
        teststand_no, module_no = self._get_no_from_event(event)

        # get the module serial from the value map
        moduleserial = self.status.get_value("moduleserial", teststand_no, module_no)

        # get the module type:
        module_type = self.value_handler.check_valid_module_serial(moduleserial)

        # display the pop up screen
        selected_test, label_map = self.display.setup_popup_test_selection(moduleserial, module_type)

        for test, result in selected_test.items():
            if result:
                # update the value map:
                self.status.update_value("selected_test", teststand_no, module_no, value=test)

                # update the displayed test name in GUI
                key = f"-TestSelection-{teststand_no}-{module_no}-"
                test_name = label_map[test]
                self.setup.update_test(key, test_name)

    def handle_back_to_base(self):

        """ This function is only used for going from test selection page to the very test stands setup page.
        """

        # hide the test selection page
        self.setup.hide_tests_selection_setup()

        #delete the previous test_selection_setup
        self.setup.destroy_test_selection_setup()
        
        for key in self.setup.window.AllKeysDict:
            print(key)

        # unhide the teststand setup page
        self.setup.show_teststands_setup()



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
    
    def _update_temp_value_map(self):
        """Helper function for updating the temp_value_map for future usage.
        """
        for teststand_no in range(1, MAX_TESTSTAND_NUM+1):
            is_selected = self.status.get_status("is_selected", teststand_no)

            if is_selected:
                fpgahostname = self.value_handler.get_fpgahostname(teststand_no)
                self.status.update_value("fpgahostname", teststand_no, value=fpgahostname)

                for module_no in range(1, MAX_MODULE_NUM+1):
                    moduleserial = self.value_handler.get_module_serial(teststand_no, module_no)

                    if moduleserial != '':
                        self.status.update_value("moduleserial", teststand_no, module_no, value=moduleserial)
    
    def _update_default_test(self, temp_value_maps):
        """Helper function for updating the default input.
           - test selection key:        "-TestSelection-{teststand_no}-{module_no}-"
           - test selection button key: "-TestSelectionButton-{teststand_no}-{module_no}-"
        """
        for teststand_no in range(1, MAX_TESTSTAND_NUM+1):
            fpgahostname = self.status.get_value("fpgahostname", teststand_no)

            # if not fpgahostname:
            #     for module_no in range(1, MAX_MODULE_NUM+1):
            #         keys = [f"-TestSelection-{teststand_no}-{module_no}-", f"-TestSelectionButton-{teststand_no}-{module_no}-"]
            #         for key in keys:
            #             self.setup.disable_key(key)

            if fpgahostname:
                for module_no in range(1, MAX_MODULE_NUM+1):
                    moduleserial = self.value_handler.get_module_serial(teststand_no, module_no)

                    if moduleserial:
                        key = f"-TestSelection-{teststand_no}-{module_no}-"
                        test = "Standard Test Procedure"
                        self.setup.update_test(key, test)
                    else:
                        keys = [f"-TestSelection-{teststand_no}-{module_no}-", f"-TestSelectionButton-{teststand_no}-{module_no}-"]
                        for key in keys:
                            self.setup.disable_key(key)