# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.configuration.config_parser import get_config_property
from version_parser import check_version, get_channel_from_version
import ast
import logging

logger = logging.getLogger(__name__)


def get_update_rules():
    return ast.literal_eval(get_config_property('Update', 'update_rules'))


def get_rule_for_current_channel(channel):
    result_list = filter(lambda x: x['channel'] == channel, get_update_rules())
    if len(result_list) == 0:
        return None
    elif len(result_list) > 1:
        print('Multiple rules for "%s" channel' % channel)
        return result_list[0]
    return result_list[0]


def is_watershed_version_required(current_version, starting_condition):
    return check_version(current_version, starting_condition)


