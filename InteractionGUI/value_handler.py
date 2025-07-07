import PySimpleGUI as sg
from InteractionGUI.state_handler import 
from global_variables import configuration

class GUIValueHandler:
    def __init__(self, window):
        self.window = window

        self.state = StateHandler(self.window)
    
    # ============================================================
    # === Value recievers ========================================
    # ============================================================
    
    def get_module_serial(self, teststand_no, module_no):
        """Get and format the module serial from the selected Scanned QR code section.
           - scanned QR code key: '-Scanned-QR-Code-{teststand_no}-{module_no}-'
        """
        key = f'-Scanned-QR-Code-{teststand_no}-{module_no}-'

        scannedcode = self.state.get_value(key)
        moduleserial = self.format_moduleserial(scannedcode)

        return moduleserial
    
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


    # ============================================================
    # === Helper functions =======================================
    # ============================================================

    def format_moduleserial(self, scannedcode):
        """Format the scanned module serial number to the standard format.
        """
        scannedcode = str(scannedcode)

        if '-' not in scannedcode:
            if len(scannedcode) >= 4:
                if scannedcode[3] == 'M':
                    moduleserial = scannedcode[0:3]+'-'+scannedcode[3:5]+'-'+scannedcode[5:9]+'-'+scannedcode[9:11]+'-'+scannedcode[11:]
                elif scannedcode[3] == 'X':
                    moduleserial = scannedcode[0:3]+'-'+scannedcode[3:5]+'-'+scannedcode[5:8]+'-'+scannedcode[8:10]+'-'+scannedcode[10:]

        else:
            moduleserial = scannedcode
        
        return moduleserial
    
    def check_valid_module_serial(self, moduleserial):
        """Check if the module serial number is valid.
        """
        passed = True   # assert every check passed

        serialsections = moduleserial.split('-')

        if len(moduleserial) >= 18:
            passed = False
        elif len(serialsections[-1]) > 4:
            passed = False
        elif len(serialsections[-1]) == 4:
            if serialsections[1][0] == 'M':
                passed = False 
        
        return passed
    
    def check_is_live(self, moduleserial):
        """Check if the module is live or not.
           - if live, return True
        """
        serialsections = moduleserial.split('-')

        # Populate scanned values 
        if serialsections[1][0] == 'M':
            is_live = True
        elif serialsections[1][0] == 'X':
            is_live = False
        else:
            raise ValueError("Invalid module serial number format.")
        
        return is_live