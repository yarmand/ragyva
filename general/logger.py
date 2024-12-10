import logging

class Logger:
  def __init__(self, name='default_logger'):
    self.logger = logging.getLogger(name)
    self.logger.setLevel(logging.ERROR)
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    handler.setFormatter(formatter)
    handler.setStream(logging.sys.stderr)
    self.logger.addHandler(handler)

  def set_level(self, level):
    self.logger.setLevel(level)

  def error(self, message):
    self.logger.error(message)

  def warning(self, message):
    self.logger.warning(message)

  def info(self, message):
    self.logger.info(message)

  def debug(self, message):
    self.logger.debug(message)

logger = Logger()
