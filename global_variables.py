import yaml

# Load configuration file
configuration = {}
with open('./configuration.yaml', 'r') as file:
    configuration = yaml.safe_load(file)
