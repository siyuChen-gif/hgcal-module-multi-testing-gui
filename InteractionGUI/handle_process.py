import PySimpleGUI as sg
from InteractionGUI.display import Display

class SetUpGUI:
    """
    This class contains all the functions that will be used to set up the BaseGUI.
    """
    def __init__(self):
        self.display = Display()

    # Functions for enabling/disabling teststand setup fields
    def toggle_all_teststands_setup(self, window, enabled):
        _, keys = self.display.setup_all_teststands()
        for key in keys:
            window[key].update(disabled=(not enabled))
    
    def enable_all_teststands_setup(self, window):
        self.toggle_all_teststands_setup(window, True)
    def disable_all_teststands_setup(self, window):
        self.toggle_all_teststands_setup(window, False)
    
    # Functions for enabling/disabling one teststand setup fields
    def toggle_one_teststand_setup(self, window, teststand_no, enable):
        _, keys = self.display.setup_single_teststand(teststand_no)
        for key in keys:
            window[key].update(disabled=(not enable))
    
    def enable_one_teststand_setup(self, window, teststand_no):
        self.toggle_one_teststand_setup(window, teststand_no, True)
    def disable_one_teststand_setup(self, window, teststand_no):
       self.toggle_one_teststand_setup(window, teststand_no, False)

    # Functions for enabling/disabling module setup fields
    def toggle_module_setup(self, enabled):
        keys = ['-DEBUG-MODE-', '-IsLive-', '-IsHB-', '-LD-', '-HD-', '-Full-', '-Top-', '-Bottom-', '-Left-', '-Right-', '-Five-', '-120-', '-200-', '-300-',
                '-Ti-', '-CF-', '-CuW-', '-Preseries-', '-V3b-2-', '-V3b-B-', '-V3b-4-', '-V3c-', '-HB-Manufacturer-', '-Module-Index-', '-FPGAHostname-', 'Configure Test Stand',
                'Only IV Test', '-Inspector-', '-Module-Status-', '-Skip-Checks-', 'Close GUI']
        for key in keys:
            basewindow[key].update(disabled=(not enabled))

    def enable_module_setup(self):
        self.toggle_module_setup(True)
    def disable_module_setup(self):
        self.toggle_module_setup(False)

    # Functions for enabling/disabling select tests fields
    def toggle_ts_tests(self, enabled):
        keys = ['-Pedestal-Run-', '-N-Pedestals-', '-Bias-Voltage-Pedestal1-', '-Bias-Voltage-Pedestal2-', '-Bias-Voltage-Pedestal3-', '-Bias-Voltage-Pedestal4-', 
                '-Bias-Voltage-Pedestal5-', '-Bias-Voltage-Pedestal6-', 'Restart Services', '-Trim-Pedestals-', '-Bias-Voltage-PedTrim-', '-Other-Script-', 
                '-Bias-Voltage-Other-', '-Standard-Test-']
        for key in keys:
            basewindow[key].update(disabled=(not enabled))

        basewindow['-Bias-Voltage-PedTrim-'].update(value='300')
        basewindow['-Bias-Voltage-Other-'].update(value='300')

    def enable_ts_tests(self):
        self.toggle_ts_tests(True)
    def disable_ts_tests(self):
        self.toggle_ts_tests(False)

    # Functions for enabling/disabling IV tests fields
    def toggle_iv_tests(self, enabled):
        keys = ['-Ambient-IV-', '-Dry-IV-', '-N-Dry-IV-', '-Dry-Wait-Bias-', '-DryIV-Wait-Time-1-', '-DryIV-Wait-Time-2-', '-DryIV-Wait-Time-3-', '-DryIV-MaxV-', '-AmbIV-MaxV-', '-StandardIV-MaxV-']
        for key in keys:
            basewindow[key].update(disabled=(not enabled))
            
    def enable_iv_tests(self):
        self.toggle_iv_tests(True)
    def disable_iv_tests(self):
        self.toggle_iv_tests(False)

    # Function to clear the values of the tests in the Select Tests section
    def clear_tests(self):
        for key in ['-Standard-Test-', '-Pedestal-Run-','-Trim-Pedestals-', '-Other-Script-', '-Ambient-IV-', '-Dry-IV-']:
            basewindow[key].update(False)
        for key in ['-N-Pedestals-', '-Bias-Voltage-Pedestal1-', '-Bias-Voltage-Pedestal2-', '-Bias-Voltage-Pedestal3-', '-Bias-Voltage-Pedestal4-', '-Bias-Voltage-Pedestal5-', '-Bias-Voltage-Pedestal6-', '-Bias-Voltage-PedTrim-', '-Bias-Voltage-Other-']:
            basewindow[key].update('')
        basewindow['-Bias-Voltage-PedTrim-'].update(value='300')
        basewindow['-Bias-Voltage-Other-'].update(value='300')
        basewindow['-DryIV-MaxV-'].update(value=f'{default_max_V}')
        basewindow['-AmbIV-MaxV-'].update(value=f'{default_max_V}')
        basewindow['-StandardIV-MaxV-'].update(value=f'{default_max_V}')

    # Function for exiting the tests and resetting the values
    def exit_tests(self):
        # After tests run, check status of services
        if current_state['-Hexactrl-Accessed-']:
            check_services(current_state)

        # Reset test values
        clear_tests()

        # Turn off HV output if live module
        if current_state['-Live-Module-'] and not current_state['-Debug-Mode-']:
            current_state['ps'].outputOff()
            update_state(current_state, '-HV-Output-On-', False, 'black')
            
        basewindow['Run Tests'].update(disabled=False)
    
    # Function to clear the values entered into the Module Setup section
    def clear_setup(self):
        event, values = basewindow.read(timeout=10)
        moduleindex = ''
        basewindow['-Module-Index-'].update('')
        basewindow['-Inspector-'].update('')
        basewindow['-Module-Status-'].update('')

        if values['-IsLive-']:
            moduleserial = f'320-{empty.join(majortype)}-{empty.join(minortype)}-{macserial}-{moduleindex}'
        elif values['-IsHB-']:
            moduleserial = f'320-{empty.join(majortype)}-{empty.join(minortype)}-{vendorid}-{moduleindex}'
        else:
            moduleserial = ''
            
        basewindow['-Module-Serial-'].update(value=moduleserial)


class DebugMode:
    """
    This class contains all the functions that will be called if it is in the debug mode.
    """
    def __init__(self):
        pass
