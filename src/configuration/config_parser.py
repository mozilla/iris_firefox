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

        except EOFError:
            logger.warning('Config file error.')
        return None
    logger.warning('Config file not found.')
    return None


def get_config_property(section, prop):
    """Returns the config property for a specific section."""
    logger.debug('Extracting {} for section {}'.format(prop, section))
    section_dict = get_config_section(section)
    if section_dict is not None:
        try:
            return section_dict[prop]
        except KeyError:
            logger.warning('Property \'{}\' not found in section {}'.format(prop, section))
            return None


def validate_section(section):
    """Validate a config.ini section."""
    err_msg = ''
    section_dict = get_config_section(section)
    if section_dict is None:
        return '[{}] section not found in [config.ini]'.format(section)
    else:
        invalid_list = []
        for key in section_dict:
            if len(str(section_dict[key]).strip()) == 0:
                invalid_list.append(key)
        if len(invalid_list) > 0:
            err_msg = '[{}] section has properties with no values: [{}]'.format(section, ', '.join(invalid_list))
    return err_msg


def validate_config_ini(args):
    if args.email:
        email_s = validate_section('Email')
        if len(email_s) > 0:
            logger.warning('{}. Submit email report was disabled.'.format(email_s))
            args.email = False
