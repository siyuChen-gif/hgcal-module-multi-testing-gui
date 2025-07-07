import re

def format_moduleserial(scannedcode):
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

print(format_moduleserial('320XLF42MH00227'))

def check_valid_module_serial(moduleserial):
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
print(check_valid_module_serial(format_moduleserial('320MLF3W2CM0105')))