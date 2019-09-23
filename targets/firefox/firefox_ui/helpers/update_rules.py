# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import ast
import logging

from moziris.configuration.config_parser import get_config_property
from moziris.api.os_helpers import OSHelper
from targets.firefox.firefox_ui.helpers.version_parser import check_version

logger = logging.getLogger(__name__)


def get_update_rules():
    """Returns the 'update_rules' config property from the 'Update' section."""
    rules = get_config_property('Update', 'update_rules')
    if rules is None:
        return None
    return ast.literal_eval(rules)


def get_rule_for_channel(channel, current_version):
    """
    :param channel: Firefox channel.
    :param current_version: Current Firefox version.
    :return: Channel's list of rules.
    """
    rules = get_update_rules()
    if rules is None:
        return None

    result_list = [x for x in rules if x['channel'] == channel and OSHelper.get_os() in x['os'] and
                   check_version(current_version, x['starting_condition'])]
    if len(result_list) == 0:
        return None
    elif len(result_list) > 1:
        logger.warning('Multiple rules for \'{}\' channel'.format(channel))
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
