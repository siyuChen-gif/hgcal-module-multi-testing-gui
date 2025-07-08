from InteractionGUI.value_handler import GUIValueHandler

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import PySimpleGUI as sg
from FPGATestStand import FPGATestStand
from ExternalPC import ExternalPC, check_hexactrl_sw
from Keithley2410 import Keithley2410
from time import sleep, time
import os
import traceback
import multiprocessing, signal
from multiprocessing import Process, Manager, active_children
from datetime import datetime

# Constants:
MAX_TESTSTAND_NUM = 8
MAX_MODULE_NUM = 3


class GUIStatusModel:
    def __init__(self, window):
        # initialize the value handler
        self.value_handler = GUIValueHandler(window)

        # set up flags
        self.flags = {
            teststand_no: {
                "teststand_flags": {
                    "is_selected": False,
                    "box_closed": False,                   # True if box is closed
                    "hexacontroller_connected": False,
                    "hexacontroller_powered": False,
                    "hexacontroller_accessed": False,
                    "firmware_loaded": False,
                    "DAQ_server": False,
                    "I2C_server": False,
                    "DAQ_client": False
                },
                "module_flags": {
                    module_no: {
                        "serial_passed": False,
                        "is_live_module": False,
                        "skip_electrical_checks": False,
                        "electrical_checks": False,         # True if checks passed or skipped
                        "only_iv_test": False,
                        "hv_connceted": False,
                        "hv_output_on": False,
                        "dcdc_lv_connected": False,
                        "dcdc_lv_powered": False,
                        "trophy_connected": False
                    } for module_no in range(1, MAX_MODULE_NUM + 1)
                }
            } for teststand_no in range(1, MAX_TESTSTAND_NUM + 1)
        }

        self.temp_value_maps = {
            teststand_no: {
                "teststand_values": {
                    "fpgahostname": None
                },
                "module_values": {
                    module_no: {
                        "moduleserial": None,
                        "selected_test": None
                    } for module_no in range(1, MAX_MODULE_NUM + 1)
                }
            } for teststand_no in range(1, MAX_TESTSTAND_NUM + 1)
        }

        # set up devices
        self.devices = {
            "pc": None,
            "ps": None
        }
        self.devices.update({
            teststand_no: {"ts": None}
            for teststand_no in range(1, MAX_TESTSTAND_NUM + 1)
        })

    # ============================================================
    # === Helper functions =======================================
    # ============================================================

    def update_status(self, key, teststand_no, module_no=None, value=True):
        """Update status of a teststand or a module.
        """
        if module_no is not None:
            self.flags[teststand_no]["module_flags"][module_no][key] = value
        else:
            self.flags[teststand_no]["teststand_flags"][key] = value

    def get_status(self, key, teststand_no, module_no=None):
        """Get status of a teststand or a module.
        """
        if module_no is not None:
            return self.flags[teststand_no]["module_flags"][module_no].get(key, False)
        else:
            return self.flags[teststand_no]["teststand_flags"].get(key, False)
    
    def update_value(self, key, teststand_no, module_no=None, value=None):
        """Update status of a teststand or a module.
        """
        if module_no is not None:
            self.temp_value_maps[teststand_no]["module_values"][module_no][key] = value
        else:
            self.temp_value_maps[teststand_no]["teststand_values"][key] = value

    def get_value(self, key, teststand_no, module_no=None):
        """Get status of a teststand or a module.
        """
        if module_no is not None:
            return self.temp_value_maps[teststand_no]["module_values"][module_no].get(key, None)
        else:
            return self.temp_value_maps[teststand_no]["teststand_values"].get(key, None)
    
    def fetch_given_flag(self, teststand_no, module_no=None):
        """Return the combined flags for a given teststand/module.
        """
        ts_flags = self.flags[teststand_no]["teststand_flags"]

        if module_flags:
            module_flags = self.flags[teststand_no]["module_flags"][module_no]
            output_flag = {
                "teststand_flags": ts_flags,
                "module_flags": module_flags
                }
        else:
            output_flag = {"teststand_flags": ts_flags}
        
        return output_flag


    # ============================================================
    # === Status Update  =========================================
    # ============================================================

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

    def end_session(self, teststand_no, module_no): # need to modify a little bit before copy and paste
        """
        Ends the testing session. The state of the testing system is contained in the `state` dictionary; this 
        function uses those flags to tell the user what must be done (and in what order) to safely shut down the
        system. In general, shutting it down broadly follows five steps:
            - Disabling the HV power
            - De-powering the DCDC or Low Voltage Supply
            - Shutting down the FPGA
            - De-powering the FPGA
            - Disconnecting all of the parts and the module
        """
        ending = display.waiting_window("Ending session...")
        sleep(2)

    def initial_module_checks(self, teststand_no, module_no):
        """
        Runs the initial checks on a module to ensure that it is ready to run the test.
        """
        try:
            if not DEBUG_MODE:
                check_hexactrl_sw()
        except AssertionError:
            ending = waiting_window("Can't find hexactrl-sw on PC. Exiting...", title="Error on PC")
            sleep(2)
            ending.close()
            self.end_session(teststand_no, module_no)
            return 'END'
        
        if self.get_status("skip_electrical_checks", teststand_no, module_no):
            self.update_status("electrical_checks", teststand_no, module_no)
        else:
            # steps to do the electrical checks
            electrical_checks = True

            self.update_status("electrical_checks", teststand_no, module_no, value=electrical_checks)

        if self.get_status("is_live_module", teststand_no, module_no):
            pass
            
        # steps to continue the checks
    
    def connect_HV(self, teststand_no, module_no):
        """Connect the HV power to the module.
        """
        if self.get_status("hv_connceted", teststand_no, module_no):
            display.do_something_window("Connect HV cable to hexaboard", "Connected", title="Connect HV")
            self.update_status("hv_connceted", teststand_no, module_no)
        
        if not self.devices['ps']:
            keith = display.waiting_window('Connecting to Keithley...', description=f'Initialize PyVISA Resource {configuration["HVResource"]}')
            if DEBUG_MODE:
                sleep(5)
                self.devices['ps'] = 1
            else:
                try:
                    self.devices['ps'] = Keithley2410()
                except:
                    self.devices['ps'] = Keithley2410()
            keith.close()

    def check_leakage_current(self, teststand_no, module_no):
        # didn't fully understand this part, pass at the moment
        pass

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
            "Temp": None
        }
        self.value_map.update({
            teststand_no: self.teststands[teststand_no].value_map
            for teststand_no in self.ready_to_run.keys()
        })

    def update_temp_humidity(self):
        """Update the temperature and humidity values for all teststands and modules.
        """
        from DBTools import add_RH_T
        self.value_map["RH"], self.value_map["Temp"] = add_RH_T()