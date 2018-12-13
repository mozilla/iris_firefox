# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.api.core.pattern import Pattern


class AboutPreferences(object):
    PRIVACY_AND_SECURITY_BUTTON_SELECTED = Pattern('category-privacy_button_selected.png')
    PRIVACY_AND_SECURITY_BUTTON_NOT_SELECTED = Pattern('category-privacy_button_not_selected.png')

    class Privacy(object):
        pass
