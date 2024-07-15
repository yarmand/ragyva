import configparser

DEFAULT_CONFIG_FILE = "'config.ini'"

global config_file
config_file = DEFAULT_CONFIG_FILE

def set_config_file(file):
  global config_file
  config_file = file

def set_default_config():
  global config_file
  config_file = DEFAULT_CONFIG_FILE

config = False
def getconfig(section, key):
  global config
  if config == False:
    config = configparser.ConfigParser()
    config.read(config_file)
  return dict(config.items(section))[key]