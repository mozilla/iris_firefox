# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import logging
import os.path
from configparser import ConfigParser
from iris2.src.core.api.errors import ConfigError
from iris2.src.core.util.path_manager import PathManager

logger = logging.getLogger(__name__)

config_file = os.path.join(PathManager.get_module_dir(), 'config.ini')
config = ConfigParser()


def get_config_property(section, prop):
    """Returns the config property for a specific section.

    :param section: Section from the config.ini file.
    :param prop: Property of a specific section.
    :return: Config property.
    """
    logger.debug('Extracting %s for section %s' % (prop, section))
    if os.path.isfile(config_file):
        try:
            config.read(config_file)
            if config.has_section(section):
                result = config.get(section, prop)
                return result
            else:
                raise ConfigError('Section %s not found' % section)
        except EOFError:
            raise ConfigError('Config file error.')
    else:
        raise ConfigError('Config file not found.')
