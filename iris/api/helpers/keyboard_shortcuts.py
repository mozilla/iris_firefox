# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import logging
import time

from iris.api.core.errors import FindError, APIHelperError
from iris.api.core.firefox_ui.library_menu import SidebarBookmarks
from iris.api.core.firefox_ui.location_bar import LocationBar
from iris.api.core.key import Key, KeyModifier, key_down, key_up, type
from iris.api.core.location import Location
from iris.api.core.pattern import Pattern
from iris.api.core.region import Region, click, drag_drop, find, wait, wait_vanish
from iris.api.core.settings import *

logger = logging.getLogger(__name__)

"""Helper details

This helper defines keyboard shortcuts for many common actions in Firefox usage.
We should be using these keyboard shortcuts whenever possible.

Try to keep them organized by area of influence
Roughly follow the organization from
https://support.mozilla.org/en-US/kb/keyboard-shortcuts-perform-firefox-tasks-quickly

- Navigation
- Current Page
- Editing
- Search
- Windows & Tabs
- History & Bookmarks
- Tools

Keyboard shortcuts for Navigation.
"""


def navigate_back():
    """Navigate back in browsing history one page visit."""
    if Settings.get_os() == Platform.MAC:
        type(text='[', modifier=KeyModifier.CMD)
    else:
        type(text=Key.LEFT, modifier=KeyModifier.ALT)


def navigate_forward():
    """Navigate forward in browsing history one page visit."""
    if Settings.get_os() == Platform.MAC:
        type(text=']', modifier=KeyModifier.CMD)
    else:
        type(text=']', modifier=KeyModifier.ALT)


def navigate_home():
    """Navigate the browser to whatever is set as the Home page."""
    type(text=Key.HOME, modifier=KeyModifier.ALT)


def open_file_picker():
    """Open the system file picker."""
    if Settings.get_os() == Platform.MAC:
        type(text='o', modifier=KeyModifier.CMD)
    else:
        type(text='o', modifier=KeyModifier.CTRL)


def select_location_bar():
    """Set focus to the location bar."""
    if Settings.get_os() == Platform.MAC:
        type(text='l', modifier=KeyModifier.CMD)
    else:
        type(text='l', modifier=KeyModifier.CTRL)
    # Wait to allow the location bar to become responsive.
    time.sleep(Settings.UI_DELAY)


def reload_page():
    """Reload the current web page."""
    if Settings.get_os() == Platform.MAC:
        type(text='r', modifier=KeyModifier.CMD)
    else:
        type(text='r', modifier=KeyModifier.CTRL)


def force_reload_page():
    """Reload the current web page with cache override."""
    if Settings.get_os() == Platform.MAC:
        type(text='r', modifier=KeyModifier.CMD + KeyModifier.SHIFT)
    else:
        type(text='r', modifier=KeyModifier.CTRL + KeyModifier.SHIFT)


def stop_page_load():
    """Stop the current in progress web page from loading."""
    type(text=Key.ESC)


# End of Navigation keyboard shortcuts.

# Keyboard shortcuts for Current Page.

def scroll_down(num=1):
    """Scroll down one increment (equivalent to 3 mousewheel steps).

    :param num: The Number of times to scroll down.
    :return: None.
    """
    for x in range(num):
        type(text=Key.DOWN)


def scroll_up(num=1):
    """Scroll up one increment (equivalent to 3 mousewheel steps).

    :param num: The number of times to scroll up.
    :return: None.
    """
    for x in range(num):
        type(text=Key.UP)


def page_down():
    """Jump down one screen."""
    type(text=Key.SPACE)


def page_up():
    """Jump up one screen."""
    type(text=Key.SPACE, modifier=KeyModifier.SHIFT)


def page_end():
    """Jump to the bottom of the page."""
    type(text=Key.END)


def page_home():
    """Jump to the top of the page."""
    type(text=Key.HOME)


def focus_next_item():
    """Focus next actionable item."""
    type(text=Key.TAB)


def focus_previous_item():
    """Focus previous actionable item."""
    type(text=Key.TAB, modifier=KeyModifier.SHIFT)


def next_frame():
    """Move to the next frame (can be in content or in chrome)."""
    type(text=Key.F6)


def previous_frame():
    """Move to the previous frame (can be in content or in chrome)."""
    type(text=Key.F6, modifier=KeyModifier.SHIFT)


def open_print_page():
    """Open the Print dialog."""
    if Settings.get_os() == Platform.MAC:
        type(text='p', modifier=KeyModifier.CMD)
    else:
        type(text='p', modifier=KeyModifier.CTRL)


def open_save_page():
    """Open the Save dialog."""
    if Settings.get_os() == Platform.MAC:
        type(text='s', modifier=KeyModifier.CMD)
    else:
        type(text='s', modifier=KeyModifier.CTRL)


def zoom_in():
    """Zoom in one increment."""
    if Settings.get_os() == Platform.MAC:
        type(text='+', modifier=KeyModifier.CMD)
    else:
        type(text='+', modifier=KeyModifier.CTRL)


def zoom_out():
    """Zoom out one increment."""
    if Settings.get_os() == Platform.MAC:
        type(text='-', modifier=KeyModifier.CMD)
    else:
        type(text='-', modifier=KeyModifier.CTRL)


def restore_zoom():
    """Restores zoom level to page default."""
    if Settings.get_os() == Platform.MAC:
        type(text='0', modifier=KeyModifier.CMD)
    else:
        type(text='0', modifier=KeyModifier.CTRL)


# End of Current Page keyboard shortcuts.

# Keyboard shortcuts for Editing.

def edit_copy():
    """Copy selection to clipboard."""
    if Settings.get_os() == Platform.MAC:
        type(text='c', modifier=KeyModifier.CMD)
    else:
        type(text='c', modifier=KeyModifier.CTRL)


def edit_cut():
    """Cut selection to clipboard."""
    if Settings.get_os() == Platform.MAC:
        type(text='x', modifier=KeyModifier.CMD)
    else:
        type(text='x', modifier=KeyModifier.CTRL)


def edit_delete():
    """Delete selected text.

    If nothing is selected, delete previous character.
    """
    type(text=Key.DELETE)


def delete_selected_file():
    """Delete selected file/files inside a folder."""
    if Settings.get_os() == Platform.MAC:
        type(text=Key.BACKSPACE, modifier=KeyModifier.CMD)
    elif Settings.get_os_version() == 'win7':
        type(text=Key.DELETE)
        type(text='y')
    else:
        type(text=Key.DELETE)


def edit_paste():
    """Paste contents of the clipboard to the focused text field."""
    if Settings.get_os() == Platform.MAC:
        type(text='v', modifier=KeyModifier.CMD)
    else:
        type(text='v', modifier=KeyModifier.CTRL)


def edit_paste_plain():
    """Paste contents of the clipboard, as plain text, to the focused text field."""
    if Settings.get_os() == Platform.MAC:
        type(text='v', modifier=KeyModifier.CMD + KeyModifier.SHIFT)
    else:
        type(text='v', modifier=KeyModifier.CTRL + KeyModifier.SHIFT)


def edit_redo():
    """Redo the last operation of Undo."""
    if Settings.get_os() == Platform.MAC:
        type(text='z', modifier=KeyModifier.CMD + KeyModifier.SHIFT)
    else:
        type(text='z', modifier=KeyModifier.CTRL + KeyModifier.SHIFT)


def edit_select_all():
    """Selects the entire contents of focused field or page."""
    if Settings.get_os() == Platform.MAC:
        type(text='a', modifier=KeyModifier.CMD)
    else:
        type(text='a', modifier=KeyModifier.CTRL)


def edit_undo():
    """Undoes the previous operation."""
    if Settings.get_os() == Platform.MAC:
        type(text='z', modifier=KeyModifier.CMD)
    else:
        type(text='z', modifier=KeyModifier.CTRL)


# End of Editing keyboard shortcuts.

# Keyboard shortcuts for Search.

def open_find():
    """Open the find toolbar."""
    if Settings.get_os() == Platform.MAC:
        type(text='f', modifier=KeyModifier.CMD)
    else:
        type(text='f', modifier=KeyModifier.CTRL)


def find_next():
    """Find next occurrence of term, if find is already active on a search term.

    Find next (again) can also find the next occurrence of a term without opening the find toolbar.
    """
    if Settings.get_os() == Platform.MAC:
        type(text='g', modifier=KeyModifier.CMD)
    else:
        type(text='g', modifier=KeyModifier.CTRL)


def find_previous():
    """Find the previous occurrence of term, if find is already active on a search term.

    Find previous can also find the previous occurrence of a term without opening the find toolbar.
    """
    if Settings.get_os() == Platform.MAC:
        type(text='g', modifier=KeyModifier.CMD + KeyModifier.SHIFT)
    else:
        type(text='g', modifier=KeyModifier.CTRL + KeyModifier.SHIFT)


def quick_find():
    """Quick find opens simple find toolbar that remains active for only six seconds."""
    if Settings.get_os() == Platform.MAC:
        type(text='/', modifier=KeyModifier.CMD)
    else:
        type(text='/', modifier=KeyModifier.CTRL)


def quick_find_link():
    """Quick find opens simple find link toolbar that remains active for only six seconds."""
    if Settings.get_os() == Platform.MAC:
        type(text="'", modifier=KeyModifier.CMD)
    else:
        type(text="'", modifier=KeyModifier.CTRL)


def close_find():
    """Close the regular find toolbar or quick find toolbar, if it has focus."""
    type(text=Key.ESC)


def select_search_bar():
    """If the search bar is present, select the search bar, otherwise this selects the location bar."""
    if Settings.get_os() == Platform.MAC:
        type(text='k', modifier=KeyModifier.CMD)
    else:
        type(text='k', modifier=KeyModifier.CTRL)


def change_search_next():
    """If the search bar has focus, change the search engine to the next in the list.

    (side effect: this also opens the search engine manager, if it wasn't already open).
    """
    if Settings.get_os() == Platform.MAC:
        type(text=Key.DOWN, modifier=KeyModifier.CMD)
    else:
        type(text=Key.DOWN, modifier=KeyModifier.CTRL)


def change_search_previous():
    """If the search bar has focus, change the search engine to the previous in the list.

    (side effect: this also opens the search engine manager, if it wasn't already open).
    """
    if Settings.get_os() == Platform.MAC:
        type(text=Key.UP, modifier=KeyModifier.CMD)
    else:
        type(text=Key.UP, modifier=KeyModifier.CTRL)


def open_search_manager():
    """If the search bar has focus, open the search engine manager."""
    type(text=Key.DOWN, modifier=KeyModifier.ALT)


# End of Search keyboard shortcuts.


# Keyboard shortcuts for Windows & Tabs.

def close_tab():
    """Close the currently focused tab/window (Except for app tabs)."""
    if Settings.get_os() == Platform.MAC:
        type(text='w', modifier=KeyModifier.CMD)
    else:
        type(text='w', modifier=KeyModifier.CTRL)


def close_window():
    """Close the currently focused window."""
    if Settings.get_os() == Platform.MAC:
        type(text='w', modifier=KeyModifier.CMD + KeyModifier.SHIFT)
    else:
        type(text='w', modifier=KeyModifier.CTRL + KeyModifier.SHIFT)


def force_close():
    """Move to the previous frame (can be in content or in chrome)."""
    type(text=Key.F4, modifier=KeyModifier.ALT)
    type(text='u', modifier=KeyModifier.CTRL)


def change_window_view():
    """Change the focus on another window."""
    if Settings.get_os() == Platform.MAC:
        type(text=Key.TAB, modifier=KeyModifier.CMD)
    else:
        type(text=Key.TAB, modifier=KeyModifier.ALT)


def full_screen():
    """Toggle full screen mode."""
    if Settings.get_os() == Platform.MAC:
        type(text='f', modifier=KeyModifier.CMD + KeyModifier.SHIFT)
    else:
        type(text=Key.F11)


def maximize_window():
    """Maximize the browser window to fill the screen.

    This is NOT Full Screen mode.
    """
    if Settings.is_mac():
        # There is no keyboard shortcut for this on Mac. We'll do it the old fashioned way.
        # This image is of the three window control buttons at top left of the window.
        # We have to resize the window to ensure maximize works properly in all cases.
        window_controls_pattern = Pattern('window_controls.png')
        controls_location = find(window_controls_pattern)
        xcoord = controls_location.x
        ycoord = controls_location.y
        width, height = window_controls_pattern.get_size()
        drag_start = Location(xcoord + 70, ycoord + 5)
        drag_end = Location(xcoord + 75, ycoord + 5)
        drag_drop(drag_start, drag_end, 0.1)

        # Alt key changes maximize button from full screen to maximize window.
        maximize_button = window_controls_pattern.target_offset(width - 3, height / 2)
        key_down(Key.ALT)
        click(maximize_button)
        key_up(Key.ALT)

    elif Settings.is_windows():
        type(text=Key.UP, modifier=KeyModifier.WIN)
    else:
        type(text=Key.UP, modifier=KeyModifier.CTRL + KeyModifier.META)
    # Wait to allow window to be maximized.
    time.sleep(Settings.UI_DELAY)


def minimize_window():
    """Minimize the browser window to the application launch bar."""
    if Settings.get_os() == Platform.MAC:
        type(text='m', modifier=KeyModifier.CMD)
    elif Settings.get_os() == Platform.WINDOWS:
        type(text=Key.DOWN, modifier=KeyModifier.WIN)
    else:
        type(text=Key.DOWN, modifier=KeyModifier.CTRL + KeyModifier.META)
    # Wait to allow window to be minimized.
    time.sleep(Settings.UI_DELAY)


def new_tab():
    """Open a new browser tab."""
    if Settings.get_os() == Platform.MAC:
        type(text='t', modifier=KeyModifier.CMD)
    else:
        type(text='t', modifier=KeyModifier.CTRL)
    # Wait to allow new tab to be opened.
    time.sleep(Settings.FX_DELAY)


def new_window():
    """Open a new browser window."""
    if Settings.get_os() == Platform.MAC:
        type(text='n', modifier=KeyModifier.CMD)
    else:
        type(text='n', modifier=KeyModifier.CTRL)


def new_private_window():
    """Open a new private browser window."""
    if Settings.get_os() == Platform.MAC:
        type(text='p', modifier=KeyModifier.CMD + KeyModifier.SHIFT)
    else:
        type(text='p', modifier=KeyModifier.CTRL + KeyModifier.SHIFT)


def next_tab():
    """Focus the next tab (one over to the right)."""
    type(text=Key.TAB, modifier=KeyModifier.CTRL)


def previous_tab():
    """Focus the previous tab (one over to the left)."""
    type(text=Key.TAB, modifier=KeyModifier.CTRL + KeyModifier.SHIFT)


def quit_firefox():
    """Quit the browser."""

    # Wait before quiting Firefox to avoid concurrency.
    time.sleep(Settings.FX_DELAY)
    if Settings.get_os() == Platform.MAC:
        type(text='q', modifier=KeyModifier.CMD)
    elif Settings.get_os() == Platform.WINDOWS:
        type(text='w', modifier=KeyModifier.CTRL + KeyModifier.SHIFT)
    else:
        type(text='q', modifier=KeyModifier.CTRL)


def select_tab(num):
    """Select a given tab (only 1-8).

    param:  num  is a string 1-8. example: '4'.
    """
    if Settings.get_os() == Platform.MAC:
        type(text=num, modifier=KeyModifier.CMD)
    elif Settings.get_os() == Platform.WINDOWS:
        type(text=num, modifier=KeyModifier.CTRL)
    else:
        type(text=num, modifier=KeyModifier.ALT)


def select_last_tab():
    """Select the last tab."""
    if Settings.get_os() == Platform.MAC:
        type(text='9', modifier=KeyModifier.CMD)
    elif Settings.get_os() == Platform.WINDOWS:
        type(text='9', modifier=KeyModifier.CTRL + KeyModifier.SHIFT)
    else:
        type(text='9', modifier=KeyModifier.CTRL)


def toggle_audio():
    """Mute/Unmute audio."""
    type(text='m', modifier=KeyModifier.CTRL)


def undo_close_tab():
    """Re-opens the previously closed tab."""
    if Settings.get_os() == Platform.MAC:
        type(text='t', modifier=KeyModifier.CMD + KeyModifier.SHIFT)
    else:
        type(text='t', modifier=KeyModifier.CTRL + KeyModifier.SHIFT)


def undo_close_window():
    """Re-opens the previously closed browser window."""
    if Settings.get_os() == Platform.MAC:
        type(text='n', modifier=KeyModifier.CMD + KeyModifier.SHIFT)
    else:
        type(text='n', modifier=KeyModifier.CTRL + KeyModifier.SHIFT)


# End of Windows & Tabs keyboard shortcuts.

# Keyboard shortcuts for History & Bookmarks.

def history_sidebar():
    """Toggle open/close the history sidebar."""
    if Settings.get_os() == Platform.MAC:
        type(text='h', modifier=KeyModifier.CMD + KeyModifier.SHIFT)
    else:
        type(text='h', modifier=KeyModifier.CTRL)


def clear_recent_history():
    """Open the Clear Recent History dialog."""
    if Settings.get_os() == Platform.MAC:
        type(text=Key.DELETE, modifier=KeyModifier.CMD + KeyModifier.SHIFT)
    else:
        type(text=Key.DELETE, modifier=KeyModifier.CTRL + KeyModifier.SHIFT)


def bookmark_all_tabs():
    """Open the Bookmark All Tabs dialog."""
    if Settings.get_os() == Platform.MAC:
        type(text='d', modifier=KeyModifier.CMD + KeyModifier.SHIFT)
    else:
        type(text='d', modifier=KeyModifier.CTRL + KeyModifier.SHIFT)
    # Wait for the Bookmark All Tabs dialog to be opened.
    time.sleep(Settings.UI_DELAY_LONG)


def bookmark_page():
    """Bookmark the current page."""
    if Settings.get_os() == Platform.MAC:
        type(text='d', modifier=KeyModifier.CMD)
    else:
        type(text='d', modifier=KeyModifier.CTRL)
    try:
        wait(LocationBar.STAR_BUTTON_STARRED, 10)
        logger.debug('Page was successfully bookmarked')
    except FindError:
        raise APIHelperError('Page can not be bookmarked')


def bookmarks_sidebar(option):
    """Toggle open/close the bookmarks sidebar."""
    if Settings.get_os() == Platform.MAC:
        type(text='b', modifier=KeyModifier.CMD)
    else:
        type(text='b', modifier=KeyModifier.CTRL)

    bookmark_sidebar_header_pattern = SidebarBookmarks.BOOKMARKS_HEADER
    if option == 'open':
        try:
            wait(bookmark_sidebar_header_pattern, 10)
            logger.debug('Sidebar is opened.')
        except FindError:
            raise APIHelperError('Sidebar is NOT present on the page, aborting.')
    elif option == 'close':
        try:
            wait_vanish(bookmark_sidebar_header_pattern, 10)
            logger.debug('Sidebar is closed.')
        except FindError:
            raise APIHelperError('Sidebar is NOT closed, aborting.')
    else:
        raise APIHelperError('Option is not supported, aborting')


def open_library():
    """Open the Library window."""
    if Settings.get_os() == Platform.MAC:
        type(text='b', modifier=KeyModifier.CMD + KeyModifier.SHIFT)
    elif Settings.get_os() == Platform.WINDOWS:
        type(text='b', modifier=KeyModifier.CTRL + KeyModifier.SHIFT)
    else:
        type(text='o', modifier=KeyModifier.CTRL + KeyModifier.SHIFT)


# End History & Bookmarks keyboard shortcuts.

# Keyboard shortcuts for Tools.

def open_addons():
    """Open the Add-ons Manager page."""
    if Settings.get_os() == Platform.MAC:
        type(text='a', modifier=KeyModifier.CMD + KeyModifier.SHIFT)
    else:
        type(text='a', modifier=KeyModifier.CTRL + KeyModifier.SHIFT)


def open_downloads():
    """Open the Downloads dialog."""
    if Settings.get_os() == Platform.MAC:
        type(text='j', modifier=KeyModifier.CMD)
    elif Settings.get_os() == Platform.WINDOWS:
        type(text='j', modifier=KeyModifier.CTRL)
    else:
        type(text='y', modifier=KeyModifier.CTRL + KeyModifier.SHIFT)


def open_page_source():
    """Open the current page's page source."""
    if Settings.get_os() == Platform.MAC:
        type(text='u', modifier=KeyModifier.CMD)
    else:
        type(text='u', modifier=KeyModifier.CTRL)


def open_web_console():
    """Opens the Web Console."""
    if Settings.get_os() == Platform.MAC:
        type(text='k', modifier=KeyModifier.CMD + KeyModifier.ALT)
    else:
        type(text='k', modifier=KeyModifier.CTRL + KeyModifier.SHIFT)


def open_web_developer_menu():
    """
    Open the Web_developer tool.
    """
    type(text=Key.F2, modifier=KeyModifier.SHIFT)


def open_browser_console():
    """
    Opens the Browser Console.
    """
    if Settings.get_os() == "osx":
        type(text="j", modifier=KeyModifier.CMD + KeyModifier.SHIFT)
    else:
        type(text="j", modifier=KeyModifier.CTRL + KeyModifier.SHIFT)


def restart_via_console():
    """
     restarts Firefox if web console is opened
    """
    if Settings.get_os() == Platform.MAC:
        type(text='r', modifier=KeyModifier.CMD + KeyModifier.ALT)
    else:
        type(text='r', modifier=KeyModifier.CTRL + KeyModifier.ALT)

# End Tools keyboard shortcuts
