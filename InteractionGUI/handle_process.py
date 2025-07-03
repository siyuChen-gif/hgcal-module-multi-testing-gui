import PySimpleGUI as sg
from InteractionGUI.display import Display, MAX_TESTSTAND_NUM
from InteractionGUI.interaction import HumanInteraction

class SetUpGUI:
    """
    This class contains all the functions that will be auto used to set up the BaseGUI window.
    """
    def __init__(self):
        self.display = Display()
        self.human_interact = HumanInteraction()

    # Functions for disabling all teststands fields
    def disable_all_teststands_setup(self, window):
        self.human_interact.toggle_all_teststands_setup(window, False)

    # Functions for enabling/disabling teststand checkbox fields
    def toggle_all_teststands_checkboxs(self, window, checked: bool):
        for teststand_no in range(1, MAX_TESTSTAND_NUM + 1):
            window[f'-TESTSTAND-{teststand_no}-'].update(checked)
    
    def check_all_teststands_checkboxs(self, window):
        self.toggle_all_teststands_checkboxs(window, True)
    def uncheck_all_teststands_checkboxs(self, window):
        self.toggle_all_teststands_checkboxs(window, False)

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
    
    # Function to end the section
    def end_session(self, state):
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

        # read density and shape from module serial
        density = state['-Module-Serial-'].split('-')[1][1]
        shape = state['-Module-Serial-'].split('-')[2][0]
        if density == 'L':
            if shape not in ['F', 'L', 'R', 'T', 'B', '5']:
                raise NotImplementedError
        elif density == 'H':
            if shape not in ['F', 'B', 'L', 'T', 'R']:
                raise NotImplementedError
        # enabled for all because nothing in this function is shape or geometry dependent
        # beside dcdc for LF
                                
        ending = waiting_window("Ending session...")
        sleep(2)

        # First disable HV if it's on
        # This part assumes the 'ps' is instantiated; a reasonable assumption if the HV output is on
        if state['-HV-Output-On-']:
            state['ps'].outputOff()
            update_state(state, '-HV-Output-On-', False, 'black')

        # De-power and disconnect the DCDC/LV Power and Hexacontroller
        # Have to nest these steps because of shutdown order
        if state['-DCDC-Connected-']:
            if state['-DCDC-Powered-']:

                command = "Disconnect DCDC power"+(" (green)" if configuration['MACSerial'] == 'CM' else '') if density+shape == 'LF' else "Turn off low voltage power"
                button = "Depowered"
                do_something_window(command, button)
                update_state(state, '-DCDC-Powered-', False, 'black')
                
                if state['-Hexactrl-Connected-']:
                    if state['-Hexactrl-Powered-']:
                        if state['-Hexactrl-Accessed-']:
                            shutdown = waiting_window("Shutting down hexacontroller...")
                            if not state['-Debug-Mode-']:
                                state['ts'].shutdown()
                            sleep(10)
                            shutdown.close()
                            update_state(state, '-FW-Loaded-', False, 'black')
                            update_state(state, '-DAQ-Server-', False, 'black')
                            update_state(state, '-I2C-Server-', False, 'black')
                            update_state(state, '-Hexactrl-Accessed-', False, 'black')

                        # new open_box call b/c for the kria have to open box to flip switch
                        open_box(state)

                        if state['-FPGA-Type-'] == 'Kria':
                            do_something_window("Turn off Kria hexacontroller power switch", "Switched Off")
                            update_state(state, '-Hexactrl-Powered-', False, 'black')
                            
                        do_something_window("Disconnect hexacontroller power"+(" (blue)" if configuration['MACSerial'] == 'CM' else ''), "Disconnected")
                        update_state(state, '-Hexactrl-Powered-', False, 'black')
                        
                    open_box(state)
                    
                    do_something_window("Disconnect hexacontroller from trophy", "Disconnected")
                    update_state(state, '-Hexactrl-Connected-', False, 'black')

            # Disconnect trophy, looback, and DCDC/LV Cables
            if state['-Trophy-Connected-']:
                if density+shape == 'LF':
                    do_something_window("Disconnect loopback", "Disconnected")
                do_something_window("Disconnect trophy", "Disconnected")
                update_state(state, '-Trophy-Connected-', False, 'black')
                
            command = "Disconnect DCDC" if density+shape == 'LF' else "Disconnect low voltage cables"
            do_something_window(command, "Disconnected")
            update_state(state, '-DCDC-Connected-', False, 'black')

        # Open the box (function handles if it's already open)
        open_box(state)

        # Lastly, disconnect the HV cable
        if state['-HV-Connected-']:

            do_something_window("Disconnect HV cable", "Disconnected")
            update_state(state, '-HV-Connected-', False, 'black')
            
        sleep(2)
        ending.close()
        return


class DebugMode:
    """
    This class contains all the functions that will be called if it is in the debug mode.
    """
    def __init__(self):
        pass
