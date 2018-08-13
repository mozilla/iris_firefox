# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.api.core.pattern import Pattern


class NavBar(object):
    HOME_BUTTON = Pattern('home_button.png')
    BACK_BUTTON = Pattern('back_button.png')
    FORWARD_BUTTON = Pattern('forward_button.png')
    HAMBURGER_MENU = Pattern('hamburger_menu.png')
    LIBRARY_MENU = Pattern('library_menu.png')


class LocationBar(object):
    SHOW_HISTORY_BUTTON = Pattern('show_history_button.png')
    BOOKMARK_BUTTON = Pattern('bookmark_button.png')
    BOOKMARK_SELECTED_BUTTON = Pattern('bookmark_selected_button.png')
    RELOAD_BUTTON = Pattern('reload_button.png')
