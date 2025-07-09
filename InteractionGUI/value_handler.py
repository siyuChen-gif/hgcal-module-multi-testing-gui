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
    
    def unformat_moduleserial(self, moduleserial):
        """Remove dashes from a formatted module serial number.
        """
        scannedcode = ''

        if isinstance(moduleserial, str) and '-' in moduleserial:
            scannedcode = moduleserial.replace('-', '')
        else:
            scannedcode = moduleserial
        return scannedcode
        