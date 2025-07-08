import re
import PySimpleGUI as sg
from InteractionGUI.state_handler import StateHandler

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
        key = f"-Scanned-QR-Code-{teststand_no}-{module_no}-"

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
    
    def check_valid_module_serial(self, moduleserial):
        """Check if the module serial number is valid.
        """
        pattern = r'^320-([A-Z]{2})-([A-Z0-9]+)-([A-Z]{2})-(\d+)$'
        match = re.match(pattern, moduleserial)

        if not match:
            return 'invalid'
        
        major_type = match.group(1)

        if major_type.startswith('M'):
            return 'module'
        elif major_type.startswith('X'):
            return 'hxb'
        else:
            return 'invalid'
    
    def check_is_live(self, moduleserial):
        """Check if the module is live or not.
           - if live, return True
        """
        status = self.check_valid_module_serial(moduleserial)
        is_live = False
        
        if status == 'module':
            is_live = True

        return is_live
    
    def check_is_hxb(self, moduleserial):
        """Check if the module is hxb or not.
           - if hxb, return True
        """
        status = self.check_valid_module_serial(moduleserial)
        is_hxb = False

        if status == 'hxb':
            is_hxb = True
        
        return is_hxb
        