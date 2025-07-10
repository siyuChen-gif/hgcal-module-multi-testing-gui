import re
import PySimpleGUI as sg
from InteractionGUI.setup import StateHandler
from InteractionGUI.validators import Validator

class GUIValueHandler:
    def __init__(self, window):
        self.window = window

        self.state = StateHandler(self.window)
        self.validator = Validator()
    
    # ============================================================
    # === Value recievers ========================================
    # ============================================================
    
    def get_module_serial(self, teststand_no, module_no):
        """Get and format the module serial from the selected Scanned QR code section.
           - scanned QR code key: '-Scanned-QR-Code-{teststand_no}-{module_no}-'
        """
        key = f"-Scanned-QR-Code-{teststand_no}-{module_no}-"

        scannedcode = self.state.get_value(key)
        moduleserial = self.format_moduleserial(scannedcode)

        return moduleserial
    
    def get_module_status(self, teststand_no, module_no):
        """Get the module status from the module status selection combo.
           - module status selection key: '-ModuleStatus-{teststand_no}-{module_no}-'
        """
        key = f'-ModuleStatus-{teststand_no}-{module_no}-'

        modulestatus = self.state.get_value(key)

        return modulestatus
    
    def get_fpgahostname(self, teststand_no):
        """Get the selected teststand IP address from the teststand IP selection section.
           - teststand ip selection key: "-FPGAHostname-{teststand_no}-"
        """
        key = f'-FPGAHostname-{teststand_no}-'

        fpgahostname = self.state.get_value(key)

        return fpgahostname
    
    def get_fpgatype(self, fpgahostname):
        """Get the selected FPGA type from the FPGA type selection section.
        """
        fpgatypes = configuration['FPGAType']

        for fpgatype in fpgatypes:
            if fpgatype.lower() in fpgahostname.lower():
                return fpgatype
            else:
                raise NotImplementedError

    def get_selected_tests(self, values, teststand_no, module_no, manager):
        """Get the selected tests from the test selection section.
        """
        tests_key_group = {
            'standard_test': ['-Standard-Test-', '-StandardIV-MaxV-'],
            'trim_pedestals': ['-Trim-Pedestals-', '-Bias-Voltage-PedTrim-'],
            'pedestal_run': ['-Pedestal-Run-', '-N-Pedestals-'] + [f'-Bias-Voltage-Pedestal{no}-' for no in range(1, 7)],
            'other_test': ['-Other-Script-', '-Other-Which-Script-'],
            'ambient_iv_test': ['-Ambient-IV-', '-AmbIV-MaxV-'],
            'dry_iv_test': ['-Dry-IV-', '-N-Dry-IV-', '-Dry-Wait-Bias-', '-DryIV-MaxV-'] + [f'-DryIV-Wait-Time-{no}-' for no in range(1, 4)],
            'skip_test': ['-Skip-Test-']
        }

        # switch key and group mapping
        key_to_group = {}
        for group, keys in tests_key_group.items():
            for k in keys:
                key_to_group[k] = group

        selected_tests = manager.get_module_value(teststand_no, module_no,'selected_tests')
        print(selected_tests)

        # loop over the group
        for group, keys in tests_key_group.items():
            checkbox_key = keys[0]  # assert checkbox key is the first

            if not values.get(checkbox_key, False):
                try:
                    del selected_tests[group]
                except KeyError:
                    pass
                continue

            selected_tests[group] = {}  # initiallize the group

            # loop through all keys in the grop
            for key in keys[1:]:
                val = values.get(key)

                # handle each group of tests
                if group == 'standard_test' and key == '-StandardIV-MaxV-':
                    try:
                        selected_tests[group]['max_voltage'] = int(val)
                    except (ValueError, TypeError):
                        selected_tests[group]['max_voltage'] = None

                elif group == 'trim_pedestals' and key == '-Bias-Voltage-PedTrim-':
                    try:
                        selected_tests[group]['bias_voltage'] = int(val)
                    except (ValueError, TypeError):
                        selected_tests[group]['bias_voltage'] = None

                elif group == 'pedestal_run':
                    if key == '-N-Pedestals-':
                        try:
                            selected_tests[group]['n_tests'] = int(val)
                        except (ValueError, TypeError):
                            selected_tests[group]['n_tests'] = None
                    elif key.startswith('-Bias-Voltage-Pedestal'):
                        try:
                            if 'bias_voltages' not in selected_tests[group]:
                                selected_tests[group]['bias_voltages'] = [None] * 6
                            no = int(key.split('-')[-2])
                            selected_tests[group]['bias_voltages'][no - 1] = int(val)
                        except:
                            pass

                elif group == 'other_test' and key == '-Other-Which-Script-':
                    selected_tests[group]['script_name'] = val

                elif group == 'ambient_iv_test' and key == '-AmbIV-MaxV-':
                    try:
                        selected_tests[group]['max_voltage'] = int(val)
                    except (ValueError, TypeError):
                        selected_tests[group]['max_voltage'] = None

                elif group == 'dry_iv_test':
                    if key == '-N-Dry-IV-':
                        try:
                            selected_tests[group]['n_tests'] = int(val)
                        except:
                            selected_tests[group]['n_tests'] = None
                    elif key == '-Dry-Wait-Bias-':
                        selected_tests[group]['bias_in_wait'] = bool(val)
                    elif key == '-DryIV-MaxV-':
                        try:
                            selected_tests[group]['max_voltage'] = int(val)
                        except:
                            selected_tests[group]['max_voltage'] = None
                    elif key.startswith('-DryIV-Wait-Time-'):
                        try:
                            if 'wait_times' not in selected_tests[group]:
                                selected_tests[group]['wait_times'] = [None] * 3
                            no = int(key.split('-')[-2])
                            selected_tests[group]['wait_times'][no - 1] = int(val)
                        except:
                            pass

                elif group == 'skip_test':
                    selected_tests[group]['skip'] = True

        # if skip is selected, only keep the skip
        if selected_tests.get('skip_test', {}).get('skip'):
            selected_tests = {
                'skip_test': selected_tests['skip_test']
            }

        manager.update_module_value(teststand_no, module_no, 'selected_tests', selected_tests)

        return selected_tests
            



    # ============================================================
    # === Helper functions =======================================
    # ============================================================

    def format_moduleserial(self, scannedcode):
        """Format the scanned module serial number to the standard format.
        """
        scannedcode = str(scannedcode)
        moduleserial = ''

        if '-' not in scannedcode:
            if len(scannedcode) >= 4:
                if scannedcode[3] == 'M':
                    moduleserial = scannedcode[0:3]+'-'+scannedcode[3:5]+'-'+scannedcode[5:9]+'-'+scannedcode[9:11]+'-'+scannedcode[11:]
                elif scannedcode[3] == 'X':
                    moduleserial = scannedcode[0:3]+'-'+scannedcode[3:5]+'-'+scannedcode[5:8]+'-'+scannedcode[8:10]+'-'+scannedcode[10:]
        else:
            moduleserial = scannedcode
        
        return moduleserial
    
    def unformat_moduleserial(self, moduleserial):
        """Remove dashes from a formatted module serial number.
        """
        scannedcode = ''

        if isinstance(moduleserial, str) and '-' in moduleserial:
            scannedcode = moduleserial.replace('-', '')
        else:
            scannedcode = moduleserial

        return scannedcode
        