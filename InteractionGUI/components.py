class Teststand:
    def __init__(self, teststand_no):
        self.teststand_no = teststand_no

        self.status_map = {
            'is_seleceted': False,
        }

        self.value_map = {
            'fpgahostname': None,
            'fpgatype': None
        }
    
    def update_status(self, status_name, status_value):
        self.status_map[status_name] = status_value
    
    def get_status(self, status_name):
        return self.status_map[status_name]

    def update_value(self, value_name, value_value):
        self.value_map[value_name] = value_value
    
    def get_value(self, value_name):
        return self.value_map[value_name]




class Module:
    def __init__(self, teststand_no, module_no):
        self.teststand_no = teststand_no
        self.module_no = module_no

        self.status_map = {
            'serial_passed': False,
            'is_live': False,
            'is_hxb': False
        }

        self.value_map = {
            'moduleserial': None,
            'module_type': None,
            'selected_test': None,
        }
    
    def update_status(self, status_name, status_value):
        self.status_map[status_name] = status_value
    
    def get_status(self, status_name):
        return self.status_map[status_name]
        
    def update_value(self, value_name, value_value):
        self.value_map[value_name] = value_value
    
    def get_value(self, value_name):
        return self.value_map[value_name]


class LiveModule(Module):
    def __init__(self, teststand_no, module_no):
        super().__init__(teststand_no, module_no)
        self.update_status('is_live', True)
        self.update_value('module_type', 'live')

class Hexaboard(Module):
    def __init__(self, teststand_no, module_no):
        super().__init__(teststand_no, module_no)
        self.update_status('is_hxb', True)
        self.update_value('module_type', 'hxb')
