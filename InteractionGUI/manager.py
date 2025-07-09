from InteractionGUI.components import Teststand, Module, LiveModule, Hexaboard

class ComponentManager:
    def __init__(self):
        self.teststands = {}  # key: teststand_no, value: Teststand object
        self.modules = {}     # key: (teststand_no, module_no), value: Module object


    # ============================================================
    # === Teststand  =============================================
    # ============================================================ 

    def create_teststand(self, teststand_no):
        if teststand_no not in self.teststands:
            self.teststands[teststand_no] = Teststand(teststand_no)

    def get_teststand(self, teststand_no):
        return self.teststands.get(teststand_no)
    
    def get_all_teststands(self):
        return self.teststands.values()

    def update_teststand_value(self, teststand_no, value_name, value):
        ts = self.get_teststand(teststand_no)
        if ts:
            ts.update_value(value_name, value)
    
    def get_teststand_value(self, teststand_no, value_name):
        ts = self.get_teststand(teststand_no)
        if ts:
            return ts.get_value(value_name)
    
    def update_teststand_status(self, teststand_no, status_name, value):
        ts = self.get_teststand(teststand_no)
        if ts:
            ts.update_status(status_name, value)
    
    def get_teststand_status(self, teststand_no, status_name):
        ts = self.get_teststand(teststand_no)
        if ts:
            return ts.get_status(status_name)
    
    def delete_teststand(self, teststand_no):
        if teststand_no in self.teststands:
            del self.teststands[teststand_no]

            # also remove the modules in this teststand
            self.modules = {
                (ts_no, m_no): m for (ts_no, m_no), m in self.modules.items()
                if ts_no != teststand_no
            }


    # ============================================================
    # === Module  ================================================
    # ============================================================ 

    def create_module(self, module_type, teststand_no, module_no):
        self.create_teststand(teststand_no)  # Ensure TS exists first
        key = (teststand_no, module_no)
        if key not in self.modules:
            if module_type == 'live':
                self.modules[key] = LiveModule(teststand_no, module_no)
            elif module_type == 'hxb':
                self.modules[key] = Hexaboard(teststand_no, module_no)

    def get_module(self, teststand_no, module_no):
        return self.modules.get((teststand_no, module_no))
    
    def get_all_modules_in_ts(self, teststand_no):
        return [
            m for (ts_no, _), m in self.modules.items() 
            if ts_no == teststand_no
        ]

    def update_module_status(self, teststand_no, module_no, status_name, value):
        module = self.get_module(teststand_no, module_no)
        if module:
            module.update_status(status_name, value)
    
    def get_module_status(self, teststand_no, module_no, status_name):
        module = self.get_module(teststand_no, module_no)
        if module:
            return module.get_status(status_name)
    
    def update_module_value(self, teststand_no, module_no, value_name, value):
        module = self.get_module(teststand_no, module_no)
        if module:
            module.update_value(value_name, value)
    
    def get_module_value(self, teststand_no, module_no, value_name):
        module = self.get_module(teststand_no, module_no)
        if module:
            return module.get_value(value_name)