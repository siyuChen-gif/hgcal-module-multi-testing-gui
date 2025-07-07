from global_variables import configuration
from InteractionGUI.value_handler import GUIValueHandler

class GUIStatusModel:
    def __init__(self):
        # initialize the value handler
        self.value_handler = GUIValueHandler()

        # set up flags
        self.flags = {
            teststand_no: {
                "is_selected": False,
                "box_closed": False,                # True if box is closed
                "hexacontroller_connected": False,
                "hexacontroller_powered": False,
                "hexacontroller_accessed": False,
                "firmware_loaded:" False,
                "DAQ_server": False,
                "I2C_server": False,
                "DAQ_client": False
                module_no: {
                    "serial_passed": False,
                    "is_live_module": False,
                    "skip_electrical_checks": False,
                    "electrical_checks": False,     # True if checks passed or skipped
                    "only_iv_test": False,
                    "hv_output_on": False,
                    "dcdc/lv_connected": False,
                    "dcdc/lv_powered": False,
                    "trophy_connected": False
                } for module_no in range(1, MAX_MODULE_NUM+1)
            } for teststand_no in range(1, MAX_TESTSTAND_NUM+1)
        } 

        # set up devices
        self.devices = {
            "pc": None,
            "ps": None,
            teststand_no: {
                "ts": None
            } for teststand_no in range(1, MAX_TESTSTAND_NUM+1)
        }
    
    def update_status(self, key, teststand_no, module_no=None, value=True):
        """Update the status of a teststand or a module with given key and value.
        """
        if module_no:
            self.flags[teststand_no][module_no][key] = value
        else:
            self.flags[teststand_no][key] = value
    
    def get_status(self, key, teststand_no, module_no=None):
        """Get the status of a teststand or a module with given key.
        """
        if module_no:
            return self.flags[teststand_no][module_no].get(key, False)
        else:
            return self.flags[teststand_no].get(key, False)

    def configure_test_stand(self, teststand_no, module_no):
        """
        Guides the user through connecting the various boards and then handles the startup of the testing system.
        """
        # get all values
        fpgahostname = value_handler.get_fpgahostname(teststand_no)
        moduleserial = value_handler.get_module_serial(teststand_no, module_no)
        fpgatype = value_handler.get_fpgatype(fpgahostname)

        # steps to configure the test stand

        if DEBUG_MODE:
            sleep(5)
            self.devices[teststand_no]['ts'] = None
        else:
            self.devices[teststand_no]['ts'] = FPGATestStand(fpgahostname, moduleserial, fpgatype)
       
        self.update_status("hexacontroller_accessed", teststand_no)

        # steps to configure the test stand

        if DEBUG_MODE:
            sleep(5)
            fwloaded = True
        else:
            fwloaded = self.devices[teststand_no]['ts'].load_firmware()
        self.update_status("firmware_loaded", teststand_no, value=fwloaded)

        # steps to configure the test stand if not fwloaded

        if DEBUG_MODE:
            sleep(5)
            services = True
        else: 
            services = self.devices[teststand_no]['ts'].startservers()
        self.update_status("DAQ_server", teststand_no, value=services)
        self.update_status("I2C_server", teststand_no, value=services)

        # steps to configure the test stand if not services

        if DEBUG_MODE:
            pc = None
            sleep(5)
        else:
            try:
                """ Might need to modify this to support 1 PCs for multiple test stands """
                self.devices["pc"] = ExternalPC(fpgahostname)   # missing import `state`
                sleep(5)
            except AssertionError:
                # steps if pc cannot be added
                raise
            
        self.update_status("DAQ_client", teststand_no)

        ready = display.waiting_window("Ready to run tests.", title="Ready")
        sleep(2)
        ready.close()


    def _check_can_run(self, teststand_no, module_no):
        """Check if a module can run the test or not.
        """
        passed = True   # assert all checks passed

        # The checkings for the modules
        # don't know yet

        return passed
    
    def check_all_ready(self):
        """Return a list of all teststands and modules that are ready to run the test.
           - output format: {1(ts): [1(m), 2(m)], 2(ts): [2(m), 3(m)]...}
        """
        ready_dict = {}

        for teststand_no in range(1, MAX_TESTSTAND_NUM + 1):
            for module_no in range(1, MAX_MODULE_NUM + 1):
                if self._check_can_run(teststand_no, module_no):
                    if teststand_no not in ready_dict:
                        ready_dict[teststand_no] = []
                    ready_dict[teststand_no].append(module_no)

        return ready_dict


class GUIContext:
    def __init__(self):
        self.ready_to_run = GUIStatusModel().check_all_ready()

        # register teststands
        self.teststands = {}
        for teststand_no in self.ready_to_run.keys():
            module_nos = self.ready_to_run[teststand_no]
            self.teststands[teststand_no] = Teststand(teststand_no, module_nos, self.devices)   # create a teststand object for each teststand
        
        # set up value map for all teststands and modules:
        self.value_map = {
            "RH": None,
            "Temp": None,
            teststand_no: {
                self.teststands[teststand_no].value_map
            } for teststand_no in self.ready_to_run.keys()
        }

        