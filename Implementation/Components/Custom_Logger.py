import logging.handlers
import time
from configparser import ConfigParser

CONFIG_FILE_PATH = ""
CONFIGURATION_FILE = CONFIG_FILE_PATH + "settings.conf"
parser = ConfigParser()
parser.read(CONFIGURATION_FILE)
LOG_PATH = parser.get('settings', 'log_path')
LOG_LEVEL = parser.get('settings','log_level')
PROJECT_NAME = parser.get("settings", "project_name")
LOG_FILE = LOG_PATH + PROJECT_NAME

logger = logging.getLogger('ArchLearner')
log_handler = logging.FileHandler(LOG_FILE + "_" + time.strftime("%Y%m%d")+'.log')
log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s',"%Y-%m-%d %H:%M:%S")
log_handler.setFormatter(log_formatter)
logger.addHandler(log_handler)
logger.setLevel(LOG_LEVEL)
logger.debug('Logger Initialized')
