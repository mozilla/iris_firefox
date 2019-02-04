# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.api.helpers.general import *
from iris.api.helpers.keyboard_shortcuts import *
from iris.api.core.key import *
from iris.api.core.settings import *


def check_preference(pref_name, value):
    """Check the value for a specific preference.

    :param pref_name: Preference to be searched.
    :param value: Preference's value to be checked.
    :return: None.
    """
    new_tab()
    select_location_bar()
    paste('about:config')
    type(Key.ENTER)
    time.sleep(Settings.UI_DELAY)

    type(Key.SPACE)
    time.sleep(Settings.UI_DELAY)

    paste(pref_name)
    time.sleep(Settings.UI_DELAY_LONG)
    type(Key.TAB)
    time.sleep(Settings.UI_DELAY_LONG)

    try:
        retrieved_value = copy_to_clipboard().split(';'[0])[1]

    except Exception as e:
        raise APIHelperError('Failed to retrieve preference value. %s' % e.message)

    if retrieved_value == value:
        return True
    else:
        return False




