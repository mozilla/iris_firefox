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

    DEFAULT_ZOOM_LEVEL = Pattern('default_zoom_level_toolbar.png')
    URL_BAR_30_ZOOM_LEVEL = Pattern('url_bar_30_zoom_level.png')
    URL_BAR_90_ZOOM_LEVEL = Pattern('url_bar_90_zoom_level.png').similar(0.7)
    URL_BAR_110_ZOOM_LEVEL = Pattern('url_bar_110_zoom_level.png')
    URL_BAR_300_ZOOM_LEVEL = Pattern('url_bar_300_zoom_level.png')


class SearchBar(object):
    SEARCH_BAR = Pattern('search_bar.png')


class FindToolbar(object):
    FIND_CLOSEBUTTON = Pattern('find_closebutton.png')
    FINDBAR_TEXTBOX = Pattern('findbar_textbox.png')
    FIND_PREVIOUS = Pattern('find_previous.png')
    FIND_NEXT = Pattern('find_next.png')
    HIGHLIGHT = Pattern('highlight.png')
    FIND_CASE_SENSITIVE = Pattern('find_case_sensitive.png')
    FIND_ENTIRE_WORD = Pattern('find_entire_word.png')
