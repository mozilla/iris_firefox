# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import logging
import os.path
from configparser import ConfigParser
from src.core.util.path_manager import PathManager

logger = logging.getLogger(__name__)

config_file = os.path.join(PathManager.get_module_dir(), 'config.ini')
config = ConfigParser()


def get_config_section(section):
    """Returns all properties of a section as a dict or None if section does not exist."""
    if os.path.isfile(config_file):
        try:
            config.read(config_file)
            if config.has_section(section):
                result = dict(config.items(section))
                return result
            else:
                logger.warning('Section {} not found'.format(section))
        except EOFError:
            logger.warning('Config file error.')
        return None
    logger.warning('Config file not found.')
    return None


def get_config_property(section, prop):
    """Returns the config property for a specific section.

    :param section: Section from the config.ini file.
    :param prop: Property of a specific section.
    :return: Config property.
    """
    logger.debug('Extracting {} for section {}'.format(prop, section))
    section_dict = get_config_section(section)
    if section_dict is not None:
        try:
            return section_dict[prop]
        except KeyError:
            logger.warning('Property \'{}\' not found in section {}'.format(prop, section))
            return None


def validate_section(section):
    section_dict = get_config_section(section)
    if section_dict is None:
        return False
    else:
        for key in section_dict:
            if len(str(section_dict[key]).strip()) == 0:
                logger.warning('Property \'{}\' from section {} has no value set'.format(key, section))
                return False
    return True
