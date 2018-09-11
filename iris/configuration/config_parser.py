import logging
import os.path
from ConfigParser import ConfigParser
from iris.api.core.errors import *
from iris.api.core.util.core_helper import get_module_dir

logger = logging.getLogger(__name__)

config_file = os.path.join(get_module_dir(), 'config.ini')
config = ConfigParser()


def get_credential(section, credential):
    logger.debug('Extracting %s for section %s' % (credential, section))
    if os.path.isfile(config_file):
        try:
            config.read(config_file)
            if config.has_section(section):
                result = config.get(section, credential)
                return result
            else:
                raise ConfigError('Section %s not found' % section)
        except EOFError:
            raise ConfigError('Config file error')
    else:
        raise ConfigError('Config file not found')
