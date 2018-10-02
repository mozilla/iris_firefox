# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.configuration.config_parser import get_config_property
from version_parser import check_version
from iris.api.core.settings import Settings
import ast
import logging

logger = logging.getLogger(__name__)


def get_update_rules():
    """Returns the 'update_rules' config property from the 'Update' section."""
    return ast.literal_eval(get_config_property('Update', 'update_rules'))


def get_rule_for_current_channel(channel, current_version):
    """
    :param channel: Firefox channel.
    :param current_version: Current Firefox version.
    :return: Channel's list of rules.
    """
    result_list = filter(
        lambda x: x['channel'] == channel and Settings.get_os() in x['os'] and
                  check_version(current_version, x['starting_condition']), get_update_rules())
    if len(result_list) == 0:
        return None
    elif len(result_list) > 1:
        logger.warning('Multiple rules for "%s" channel' % channel)
        return result_list[0]
    return result_list[0]


def is_update_required(current_version, starting_condition):
    """Check that Firefox update is required.

    :param current_version: Current Firefox version.
    :param starting_condition: Input string. Examples of accepted formats:
    '60', '>60', '<60', '>=60', '<=60', '!=60', '60-63'. A '60' version will automatically be converted into '60.0.0'.
    :return: Call the check_version() method.
    """
    return check_version(current_version, starting_condition)
