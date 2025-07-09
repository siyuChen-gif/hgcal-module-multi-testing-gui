import yaml


## -- load configuration -- ##
configuration = {}
with open('./configuration.yaml', 'r') as file:
    configuration = yaml.safe_load(file)


## -- global variables -- ##
# Debug mode
DEBUG_MODE = configuration['DebugMode']

# Constants:
MAX_TESTSTAND_NUM = 8
MAX_MODULE_NUM = 3

lgfont = ('Arial', 2*int(configuration['DefaultFontSize']))

