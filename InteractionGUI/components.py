from InteractionGUI.setup import GUISetUp

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
            'module_status': None,
            'selected_tests': None,
        }
    
    # functions
    def update_status(self, status_name, status_value):
        self.status_map[status_name] = status_value
    
    def get_status(self, status_name):
        return self.status_map[status_name]
        
    def update_value(self, value_name, value_value):
        self.value_map[value_name] = value_value
    
    def get_value(self, value_name):
        return self.value_map[value_name]

    def update_selected_tests(self, setup):
        """Update the test selection windows according
        """
        selected = self.get_value('selected_tests')
        if not selected:
            return 
        
        # === Standard Test Procedure ===
        if 'standard_test' in selected:
            setup.update_checkbox('-Standard-Test-', True)
            setup.update_value('-StandardIV-MaxV-', selected['standard_test'].get('max_voltage', ''))

        # === Trim Pedestals ===
        if 'trim_pedestals' in selected:
            setup.update_checkbox('-Trim-Pedestals-', True)
            setup.update_value('-Bias-Voltage-PedTrim-', selected['trim_pedestals'].get('bias_voltage', ''))

        # === Pedestal Run ===
        if 'pedestal_run' in selected:
            setup.update_checkbox('-Pedestal-Run-', True)
            setup.update_value('-N-Pedestals-', selected['pedestal_run'].get('n_runs', ''))
            bias_list = selected['pedestal_run'].get('bias_voltages', [])
            for i, val in enumerate(bias_list):
                key = f'-Bias-Voltage-Pedestal{i+1}-'
                setup.update_value(key, val)

        # === Other Test Script ===
        if 'other_test' in selected:
            setup.update_checkbox('-Other-Script-', True)
            setup.update_value('-Other-Which-Script-', selected['other_test'].get('script_name', ''))

        # === Ambient IV Curve ===
        if 'ambient_iv_test' in selected:
            setup.update_checkbox('-Ambient-IV-', True)
            setup.update_value('-AmbIV-MaxV-', selected['ambient_iv_test'].get('max_voltage', ''))

        # === Dry IV Curve ===
        if 'dry_iv_test' in selected:
            setup.update_checkbox('-Dry-IV-', True)
            setup.update_value('-N-Dry-IV-', selected['dry_iv_test'].get('n_runs', ''))
            setup.update_checkbox('-Dry-Wait-Bias-', selected['dry_iv_test'].get('bias_during_wait', False))
            setup.update_value('-DryIV-MaxV-', selected['dry_iv_test'].get('max_voltage', ''))
            wait_times = selected['dry_iv_test'].get('wait_times', [])
            for i, val in enumerate(wait_times):
                key = f'-DryIV-Wait-Time-{i+1}-'
                setup.update_value(key, val)

        # === Skip Test ===
        if 'skip_test' in selected:
            setup.update_checkbox('-Skip-Test-', True)


class LiveModule(Module):
    def __init__(self, teststand_no, module_no):
        super().__init__(teststand_no, module_no)
        self.update_status('is_live', True)
        self.update_value('module_type', 'live')
    
    def setup_test_selection(self, setup):
        """Initialize the test selection windows.
        """
        moduleserial = self.get_value('moduleserial')
        setup.update_value('-Tests-Text-', f'Tests to run for Live Module: {moduleserial}')

        self.update_selected_tests(setup)

class Hexaboard(Module):
    def __init__(self, teststand_no, module_no):
        super().__init__(teststand_no, module_no)
        self.update_status('is_hxb', True)
        self.update_value('module_type', 'hxb')

    def setup_test_selection(self, setup):
        """Initialize the test selection windows.
        """
        moduleserial = self.get_value('moduleserial')
        setup.update_value('-Tests-Text-', f'Tests to run for Hexaboard: {moduleserial}')

        invisibile_keys = ['-Bias-Voltage-PedTrim-Text-', '-Bias-Voltage-PedTrim-', '-BV-Menu-']
        disable_keys = ['-Ambient-IV-', '-AmbIV-MaxV-', '-Dry-IV-', '-N-Dry-IV-', '-Dry-Wait-Bias-', '-DryIV-Wait-Time-1-', '-DryIV-Wait-Time-2-', '-DryIV-Wait-Time-3-', '-DryIV-MaxV-']
        setup.hide_all_keys(invisibile_keys)
        setup.disable_all(disable_keys)

        self.update_selected_tests(setup)