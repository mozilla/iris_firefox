# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.api.core.pattern import Pattern


class AboutConfig(object):
    ACCEPT_RISK = Pattern('accept_risk.png')
    DEFAULT_STATUS_PATTERN = Pattern('default_status.png')
    MODIFIED_STATUS_PATTERN = Pattern('modified_status.png')
    ENTER_INTEGER_VALUE = Pattern('enter_integer_value.png')

    class PreferenceName(object):
        INTL_UIDIRECTION = Pattern('intl_uidirection.png')
