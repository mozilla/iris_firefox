# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.api.core.pattern import Pattern


class Tabs(object):
    NEW_TAB_HIGHLIGHTED = Pattern('tab_content_selected_new_tab.png')
    NEW_TAB_NOT_HIGHLIGHTED = Pattern('tab_content_new_tab.png')
