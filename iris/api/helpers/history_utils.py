# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
from iris.api.core.firefox_ui.library import Library
from iris.api.core.firefox_ui.nav_bar import NavBar
from iris.api.core.firefox_ui.library_menu import LibraryMenu
from iris.api.core.firefox_ui.history import History
from iris.api.helpers.test_utils import access_and_check_pattern


def open_clear_recent_history_window():
    return [
        access_and_check_pattern(NavBar.LIBRARY_MENU, '\"Library menu\"', LibraryMenu.HISTORY_BUTTON, 'click'),
        access_and_check_pattern(LibraryMenu.HISTORY_BUTTON, '\"History menu\"',
                                 History.HistoryMenu.CLEAR_RECENT_HISTORY, 'click'),
        access_and_check_pattern(History.HistoryMenu.CLEAR_RECENT_HISTORY, '\"Clear recent History\"',
                                 History.CLearRecentHistory.CLEAR_RECENT_HISTORY_TITLE, 'click')]


def open_history_library_window():
    return [
        access_and_check_pattern(NavBar.LIBRARY_MENU, '\"Library menu\"', LibraryMenu.HISTORY_BUTTON, 'click'),
        access_and_check_pattern(LibraryMenu.HISTORY_BUTTON, '\"History menu\"',
                                 History.HistoryMenu.SHOW_ALL_HISTORY, 'click'),
        access_and_check_pattern(History.HistoryMenu.SHOW_ALL_HISTORY, '\"History menu\"',
                                 Library.TITLE, 'click')]
