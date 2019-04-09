from targets.firefox.firefox_ui.general_test_utils import access_and_check_pattern
from targets.firefox.firefox_ui.history import History
from targets.firefox.firefox_ui.library import Library
from targets.firefox.firefox_ui.library_menu import LibraryMenu
from targets.firefox.firefox_ui.nav_bar import NavBar


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
