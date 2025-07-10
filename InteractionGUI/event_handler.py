from time import sleep
import PySimpleGUI as sg

from InteractionGUI.setup import GUISetUp
from InteractionGUI.display import Display
from InteractionGUI.value_handler import GUIValueHandler
from InteractionGUI.validators import Validator
from InteractionGUI.manager import ComponentManager
from InteractionGUI.global_var import *


class GUIEventHandler:
    """
    This class contains all the functions that will be auto used to handle the events of the BaseGUI window.
    """
    def __init__(self, window):
        self.setup = GUISetUp(window)
        self.value_handler = GUIValueHandler(window)
        self.display = Display()
        self.validator = Validator()
        self.manager = ComponentManager()

        # count of going back to the base window
        self.back_to_base_num = 0

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
            self.handle_popup_test_selection(event)

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
        teststand checkbox key: '-TESTSTAND-{teststand_no}-'
        """
        teststand_no, _ = self._get_no_from_event(event)
        is_checked = values.get(event, False)

        if is_checked:
            self.setup.enable_one_teststand(teststand_no)
        else:
            self.setup.disable_one_teststand(teststand_no)

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

        module_type, _ = self.validator.check_valid_module_serial(moduleserial)

        if module_type == 'live':
            mod_statuses = ['Assembled', 'Backside Bonded', 'Backside Encapsulated',
                            'Completely Bonded', 'Bonds Reworked', 'Completely Encapsulated', 'Bolted']
            self.setup.update_combo(combo_key, mod_statuses)
        elif module_type == 'hxb':
            hxb_statuses = ['Untaped', 'Taped']
            self.setup.update_combo(combo_key, hxb_statuses)
        else:
            self.setup.update_combo(combo_key, [])
        
    def handle_configure_teststand(self):
        """
        configure teststand button key: '-Configure-Test-Stand-'
        """
        # only allow click once before finishing configuration
        self.setup.disable("-Configure-Test-Stand-")

        configured = True   # assert all teststands configured

        """ Validation for All_Inputs """

        if DEBUG_MODE:
            sleep(1)
        
        if configured:
            # disable inspector
            self.setup.disable("-INSPECTOR-")

            # update the componets
            self._update_components()

            # let users know the configuration process is done
            end = self.display.waiting_window("Test stands configured.")
            sleep(1)
            end.close()
            
            # hide the configuration setup frame
            self.setup.hide_teststands_setup()

            # display the testselection frame
            self.setup.delete_tests_selection_setup()   # remove the placeholder

            TEST_SETUP_LAYOUT = self.display.setup_all_test_selection(self.manager)

            if self.back_to_base_num == 0:
                FRAME_LAYOUT = sg.Frame('Tests Selections', layout=TEST_SETUP_LAYOUT, key=self.setup.tests_selection_layout_key, visible=True)
                # add the test selection frame to the window
                self.setup.add_tests_selection_setup(FRAME_LAYOUT)
            else:
                self.setup.update_value(self.setup.tests_selection_layout_key,TEST_SETUP_LAYOUT)

            # show the frame
            self.setup.show_tests_selection_setup()

            # update the default test
            self._update_default_test()

            # enable the configuration setup button for future usage -> re-configure test stands
            self.setup.enable("-Configure-Test-Stand-")
        
    def handle_popup_test_selection(self, event):
        """
        test selection key:        "-TestSelection-{teststand_no}-{module_no}-"
        test selection button key: "-TestSelectionButton-{teststand_no}-{module_no}-"
        """
        # get the teststand and module number from the event key
        teststand_no, module_no = self._get_no_from_event(event)

        # get the module serial from the value map
        moduleserial = self.manager.get_module_value(teststand_no, module_no, "moduleserial")
        module_type = self.manager.get_module_value(teststand_no, module_no, "module_type")

        # display the pop up screen
        self.display.setup_popup_test_selection(teststand_no, module_no, self.manager)

        # update the selected test
        self._update_selected_test(teststand_no, module_no, self.manager)

    def handle_back_to_base(self):

        """ This function is only used for going from test selection page to the very test stands setup page.
        """

        # hide the test selection page
        self.setup.hide_tests_selection_setup()

        self.back_to_base_num += 1

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
    
    def _update_components(self):
        """Helper function for updating the value map for future usage.
           - teststand checkbox key: '-TESTSTAND-{teststand_no}-'
           - input box key:          '-Scanned-QR-Code-{teststand_no}-{module_no}-'
        """
        # update and create the teststand in manager:
        for teststand_no in range(1, MAX_TESTSTAND_NUM+1):
            checkbox_key = f'-TESTSTAND-{teststand_no}-'
            is_checked = self.setup.get_value(checkbox_key)

            if is_checked:
                fpgahostname = self.value_handler.get_fpgahostname(teststand_no)
                self.manager.create_teststand(teststand_no)
                self.manager.update_teststand_value(teststand_no, "fpgahostname", fpgahostname)
                self.manager.update_teststand_status(teststand_no, "is_selected", True)

                # update and create the module in manager:
                for module_no in range(1, MAX_MODULE_NUM+1):
                    moduleserial    = self.value_handler.get_module_serial(teststand_no, module_no)
                    module_status   = self.value_handler.get_module_status(teststand_no, module_no)

                    # check if the input is valid or not
                    module_type, valid = self.validator.check_valid_module_serial(moduleserial)

                    if valid:
                        self.manager.create_module(module_type, teststand_no, module_no)
                        self.manager.update_module_value(teststand_no, module_no, "moduleserial", moduleserial)
                        self.manager.update_module_value(teststand_no, module_no, "module_status", module_status)

    def _update_default_test(self):
        """Helper function for updating the default input.
           - test selection key:        "-TestSelection-{teststand_no}-{module_no}-"
           - test selection button key: "-TestSelectionButton-{teststand_no}-{module_no}-"
        """
        for teststand_no in range(1, MAX_TESTSTAND_NUM+1):
            ts = self.manager.get_teststand(teststand_no)

            # check if teststand exist:
            if ts:
                modules = self.manager.get_all_modules_in_ts(teststand_no)

                # check if there are modules in the teststands
                if modules:
                    for module_no in range(1, MAX_MODULE_NUM+1):
                        module = self.manager.get_module(teststand_no, module_no)

                        if module:
                            value = {'standard_test': {'enabled': True, 'max_voltage': 500}}
                            self.manager.update_module_value(teststand_no, module_no, 'selected_tests', value)

                            key = f"-TestSelection-{teststand_no}-{module_no}-"
                            self.setup.update_value(key, 'standard_test')

                        # disable the empty input
                        else: 
                            keys = [f"-TestSelection-{teststand_no}-{module_no}-", f"-TestSelectionButton-{teststand_no}-{module_no}-"]
                            for key in keys:
                                self.setup.disable(key)
                
                # delete the teststand object if there's no module contains
                else:
                    self.manager.delete_teststand(teststand_no)
    
    def _update_selected_test(self, teststand_no, module_no, manager):
        """Helper function for updating the selected test.
           - test selection key: "-TestSelection-{teststand_no}-{module_no}-"
        """
        key = f"-TestSelection-{teststand_no}-{module_no}-"

        selected_test = manager.get_module_value(teststand_no, module_no,'selected_tests')
        test_count = 0
        test_list = []

        for test, test_info in selected_test.items():
            if test_info:
                test_count += 1
                test_list.append(test)
        
        if test_count == 1:
            self.setup.update_value(key, test_list[0])
        else:
            self.setup.update_value(key, 'Multiple Tests')