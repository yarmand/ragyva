import configparser
      
config = False
def getconfig(section, key, config_file='config.ini'):
  global config
  if config == False:
    config = configparser.ConfigParser()
    config.read(config_file)
  return dict(config.items(section))[key]