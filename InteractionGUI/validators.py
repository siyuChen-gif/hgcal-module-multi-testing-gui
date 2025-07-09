import re

class Validator:
    def __init__(self):
        pass

    def check_valid_module_serial(self, moduleserial):
        """Check if the module serial is valid.
        """
        pattern = r'^320-([A-Z]{2})-([A-Z0-9]+)-([A-Z]{2})-(\d+)$'
        match = re.match(pattern, moduleserial)

        # Default return values
        module_type = 'invalid'
        valid = False

        if match:
            major_type = match.group(1)
            if major_type.startswith('M'):
                module_type = 'live'
                valid = True
            elif major_type.startswith('X'):
                module_type = 'hxb'
                valid = True

        return module_type, valid