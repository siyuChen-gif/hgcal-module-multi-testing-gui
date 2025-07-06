

class GUIStatusModel:
    def __init__(self):
        self.flags = {
            teststand_no: {
                "is_selected": False,
                "hexacontroller_connected": False,
                "hexacontroller_powered": False,
                "hexacontroller_accessed": False,
                "firmware_loaded:" False
                module_no: {
                    "serial_passed": False,
                    "is_live_module": False,
                    "electrical_checks": False,     # True if checks passed or skipped
                    "only_iv_test": False,
                    "box_closed": False,            # True if box is closed
                    "hv_output_on": False,
                    "dcdc/lv_connected": False,
                    "dcdc/lv_powered": False,
                    "trophy_connected": False
                } for module_no in range(1, MAX_MODULE_NUM+1)
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

    def _check_can_run(self, teststand_no, module_no):
        """Check if a module can run the test or not.
        """
        passed = True   # assert all checks passed

        # The checkings for the modules
        # don't know yet

        return passed
    
    def check_all_ready(self):
        """Return a list of all teststands and modules that are ready to run the test.
           - output format: [(ts1, m1), (ts1, m2), (ts2, m1)...]
        """
        ready_list = []

        for teststand_no in range(1, MAX_TESTSTAND_NUM+1):
            for module_no in range(1, MAX_MODULE_NUM+1):
                if self._check_can_run(teststand_no, module_no):
                    ready_list.append((teststand_no, module_no))
        
        return ready_list


class GUIContext:
    def __init__(self):
        self.value_maps = {
            teststand_no: {
                "teststand_ip": None,
                "RH": None,     # Do we assume RH and T are the same for each module?
                "Temp": None,
                module_no: {
                    "moduleserial": None,
                    "start_time": None,
                    "output_path": None,
                    "summary": None
                } for module_no in range(1, MAX_MODULE_NUM+1)
            } for teststand_no in range(1, MAX_TESTSTAND_NUM+1)
        } 