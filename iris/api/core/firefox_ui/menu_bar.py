# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.api.core.pattern import Pattern


class MenuBar(object):
    class Edit(object):
        EDIT_PATTERN = Pattern('menu_bar_edit_pattern.png')
        EDIT_FIND_IN_PAGE = Pattern('menu_bar_edit_find_in_page_pattern.png')
