
from ConfigParser import ConfigParser
import os.path
from logger.iris_logger import *



logger = getLogger(__name__)


config_file=('config.ini')

config=ConfigParser()

def get_credentials(section,credentials):
    logger.debug( "Extracting "+credentials+" for section "+section)
    if os.path.isfile(config_file):
        try:
            config.read(config_file)
            if config.has_section(section):
                result=config.get(section,credentials)
                return result
            else:
                logger.debug( 'Section not found!!!')
                return None
        except EOFError:
            logger.debug( "File Error!!!")
    else:
         logger.debug( "File Not Found!!!")
