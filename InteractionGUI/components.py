from InteractionGUI.value_handler import GUIValueHandler
from InteractionGUI.display import Display
from global_variables import configuration

DEBUG_MODE = configuration['DebugMode']

class Teststand:
    def __init__(self, teststand_no: int, module_nos: list, devices: list):
        # initialize the value handler
        self.value_handler = GUIValueHandler()
        self.display = Display()

        # get information
        self.teststand_no = teststand_no
        self.module_nos = module_nos
        self.devices = devices

        self.fpgahostname = self.value_handler.get_fpgahostname(self.teststand_no)
        self.modules = {}

        for module_no in self.module_nos:
            self.moduleserial = self.value_handler.get_module_serial(self.teststand_no, module_no)
            self.modules[module_no] = Module(self.teststand_no, self.moduleserial, self.devices)    # create a module object for each module in the teststand
            
        # set up value map for the teststand
        self.value_map = {
            "fpgahostname": self.fpgahostname,
            "fpgatype": None,
            module_no: {
                self.modules[module_no].value_map
            } for module_no in module_nos
        }



class Module:
    def __init__(self, teststand_no, moduleserial, devices):
        # initialize the value handler
        self.value_handler = GUIValueHandler()
        self.display = Display()

        # get information
        self.teststand_no = teststand_no
        self.fpgahostname = self.value_handler.get_fpgahostname(self.teststand_no)
        self.moduleserial = moduleserial
        self.devices = devices

        # set up value map for the module
        self.value_map = {
            "moduleserial": self.moduleserial,
            "start_time": None,
            "output_path": None,
            "summary": None
        }
    
    