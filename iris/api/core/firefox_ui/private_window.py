# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.api.core.pattern import Pattern


class PrivateWindow(object):
    private_window_pattern = Pattern('private_window.png')
    SEE_HOW_IT_WORKS_BUTTON = Pattern('see_how_it_works_button.png')
    TRACKING_PROTECTION_SWITCH_ON = Pattern('tracking_protection_switch_on.png')
    TRACKING_PROTECTION_SWITCH_OFF = Pattern('tracking_protection_switch_off.png')
    TRACKING_PROTECTION_SHIELD_ACTIVATED = Pattern('tracking_protection_shield_private_window_activated.png')
    TRACKING_PROTECTION_SHIELD_DEACTIVATED = Pattern('tracking_protection_shield_private_window_deactivated.png')


