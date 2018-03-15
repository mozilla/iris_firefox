
from ConfigParser import ConfigParser
import os.path
from logger.iris_logger import *



logger = getLogger(__name__)


config_file=('config.ini')

config=ConfigParser()

def get_credential(section,credential):
    logger.debug( "Extracting %s for section %s" % (credential, section))
    if os.path.isfile(config_file):
        try:
            config.read(config_file)
            if config.has_section(section):
                result=config.get(section,credential)
                return result
            else:
                logger.debug( 'Section not found')
                return None
        except EOFError:
            logger.warning( "Config file error")
            return None
    else:
         logger.error( "Config file not found")
         return None
