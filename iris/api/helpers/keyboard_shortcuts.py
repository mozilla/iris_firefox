# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import time
from api.core import hotkey_press
from api.core import press
from api.core import keyDown
from api.core import keyUp
from api.core import scroll
from api.core import get_os
from api.core import click
from api.core import type

from api.core import Key, KeyModifier

from logger.iris_logger import *

logger = getLogger(__name__)


# This helper defines keyboard shortcuts for many common actions in Firefox usage.
# We should be using these keyboard shortcuts whenever possible.
#
# Try to keep them organized by area of influence
# Roughly follow the organization from
# https://support.mozilla.org/en-US/kb/keyboard-shortcuts-perform-firefox-tasks-quickly

# - Navigation
# - Current Page
# - Editing
# - Search
# - Windows & Tabs
# - History & Bookmarks
# - Tools

# Keyboard shortcuts for Navigation.


def navigate_back():
    """
    Navigate back in browsing history one page visit.
    """
    if get_os() == "osx":
        # @todo double check on mac
        hotkey_press('alt', 'left')
    else:
        hotkey_press('alt', 'left')


def navigate_forward():
    """
    Navigate forward in browsing history one page visit.
    """
    if get_os() == "osx":
        # @todo double check on mac
        hotkey_press('alt', 'right')
    else:
        hotkey_press('alt', 'right')


def navigate_home():
    """
    Navigate the browser to whatever is set as the Home page.
    """
    hotkey_press('alt', 'home')


def open_file_picker():
    """
    Open the system file picker.
    """
    if get_os() == "osx":
        hotkey_press('command', 'o')
    else:
        hotkey_press('ctrl', 'o')


def select_location_bar():
    """
    Set focus to the locationbar.
    """
    if get_os() == "osx":
        hotkey_press('command', 'l')
    else:
        hotkey_press('ctrl', 'l')
    # wait to allow the location bar to become responsive.
    time.sleep(1)


def reload_page():
    """
    Reload the current web page.
    """
    if get_os() == "osx":
        hotkey_press('command', 'r')
    else:
        hotkey_press('ctrl', 'r')


def force_reload_page():
    """
    Reload the current web page with cache override.
    """
    if get_os() == "osx":
        hotkey_press('command', 'shift', 'r')
    else:
        hotkey_press('ctrl', 'shift', 'r')


def stop_page_load():
    """
    Stop the current in progress web page from loading.
    """
    hotkey_press('escape')


# End of Navigation keyboard shortcuts.

# Keyboard shortcuts for Current Page.

def scroll_down(clicks=3):
    """
    Scroll down one increment (equivalant to 3 mousewheel steps).
    """
    scroll(clicks)


def scroll_up(clicks=-3):
    """
    Scroll up one increment (equivalant to 3 mousewheel steps).
    """
    scroll(clicks)


def page_down():
    """
    Jump down one screen.
    """
    press("space")


def page_up():
    """
    Jump up one screen.
    """
    hotkey_press('shift', 'space')


def page_end():
    """
    Jump to the bottom of the page.
    """
    press("end")


def page_home():
    """
    Jump to the top of the page.
    """
    press("home")


def focus_next_item():
    """
    Focus next actionable item.
    """
    press("tab")


def focus_previous_item():
    """
    Focus previous actionable item.
    """
    hotkey_press("shift", "tab")


def next_frame():
    """
    Move to the next frame (can be in content or in chrome).
    """
    press("f6")


def previous_frame():
    """
    Move to the previous frame (can be in content or in chrome).
    """
    hotkey_press("shift", 'f6')


def open_print_page():
    """
    Open the Print dialog.
    """
    if get_os() == "osx":
        hotkey_press("command", "p")
    else:
        hotkey_press("ctrl", "p")


def open_save_page():
    """
    Open the Save dialog.
    """
    if get_os() == "osx":
        hotkey_press("command", "s")
    else:
        hotkey_press("ctrl", "s")


def zoom_in():
    """
    Zoom in one increment.
    """
    if get_os() == "osx":
        hotkey_press("command", "+")
    else:
        hotkey_press("ctrl", "+")


def zoom_out():
    """
    Zoom out one increment.
    """
    if get_os() == "osx":
        hotkey_press("command", "-")
    else:
        hotkey_press("ctrl", "-")


def restore_zoom():
    """
    Restores zoom level to page default.
    """
    if get_os() == "osx":
        hotkey_press("command", "0")
    else:
        hotkey_press("ctrl", "0")


# End of Current Page keyboard shortcuts.

# Keyboard shortcuts for Editing.

def edit_copy():
    """
    Copy selection to clipboard.
    """
    if get_os() == "osx":
        hotkey_press("command", "c")
    else:
        hotkey_press("ctrl", "c")


def edit_cut():
    """
    Cut selection to clipboard.
    """
    if get_os() == "osx":
        hotkey_press("command", "x")
    else:
        hotkey_press("ctrl", "x")


def edit_delete():
    """
    Delete selected text.
    If nothing is selected, delete previous character.
    """
    press("delete")


def edit_paste():
    """
    Paste contents of the clipboard to the focused text field.
    """
    if get_os() == "osx":
        hotkey_press("command", "v")
    else:
        hotkey_press("ctrl", "v")


def edit_paste_plain():
    """
    Paste contents of the clipboard, as plain text, to the focused text field.
    """
    if get_os() == "osx":
        hotkey_press("command", "shift", "v")
    else:
        hotkey_press("ctrl", "shift", "v")


def edit_redo():
    """
    Redo the last operation of Undo.
    """
    if get_os() == "osx":
        hotkey_press("command", "shift", "z")
    else:
        hotkey_press("ctrl", "shift", "z")


def edit_select_all():
    """
    Selects the entire contents of focused field or page.
    """
    if get_os() == "osx":
        hotkey_press("command", "a")
    else:
        hotkey_press("ctrl", "a")


def edit_undo():
    """
    Undoes the previous operation.
    """
    if get_os() == "osx":
        hotkey_press("command", "z")
    else:
        hotkey_press("ctrl", "z")


# End of Editing keyboard shortcuts.

# Keyboard shortcuts for Search.

def open_find():
    """
    Open the find toolbar.
    """
    if get_os() == "osx":
        hotkey_press("command", "f")
    else:
        hotkey_press("ctrl", "f")


def find_next():
    """
    Find next occurance of term if find is already active on a search term.
    Find next (again) can also find the next occurance of a term without opening the find toolbar.
    """
    if get_os() == "osx":
        hotkey_press("command", "g")
    else:
        hotkey_press("ctrl", "g")


def find_previous():
    """
    Find the previous occurance of term, if find is already active on a search term.
    Find previous can also find the previous occurance of a term without opening the find toolbar.
    """
    if get_os() == "osx":
        hotkey_press("command", "shift", "g")
    else:
        hotkey_press("ctrl", "shift", "g")


def quick_find():
    """
    Quick find opens simple find toolbar that remains active for only six seconds.
    """
    if get_os() == "osx":
        hotkey_press("command", "/")
    else:
        hotkey_press("ctrl", "/")


def quick_find_link():
    """
    Quick find opens simple find link toolbar that remains active for only six seconds.
    """
    if get_os() == "osx":
        hotkey_press("command", "'")
    else:
        hotkey_press("ctrl", "'")


def close_find():
    """
    Close the regular find toolbar or quick find toolbar, if it has focus.
    """
    press("escape")


def select_search_bar():
    """
    If the search bar is present, select the search bar, otherwise this selects the location bar.
    """
    if get_os() == "osx":
        hotkey_press("command", "k")
    else:
        hotkey_press("ctrl", "k")


def change_search_next():
    """
    If the search bar has focus, change the search engine to the next in the list.
    (side effect: this also opens the search engine manager, if it wasn't alredy open).
    """
    if get_os() == "osx":
        hotkey_press("command", "down")
    else:
        hotkey_press("ctrl", "down")


def change_search_previous():
    """
    If the search bar has focus, change the search engine to the previous in the list.
    (side effect: this also opens the search engine manager, if it wasn't already open).
    """
    if get_os() == "osx":
        hotkey_press("command", "up")
    else:
        hotkey_press("ctrl", "up")


def open_search_manager():
    """
    If the search bar has focus open the search engine manager.
    """
    hotkey_press("alt", "down")


# End of Search keyboard shortcuts.


# Keyboard shortcuts for Windows & Tabs.

def close_tab():
    """
    Close the currently focused tab (Except for app tabs).
    """
    if get_os() == "osx":
        hotkey_press("command", "w")
    else:
        hotkey_press("ctrl", "w")


def close_window():
    """
    Close the currently focused window.
    """
    if get_os() == "osx":
        hotkey_press("command", "shift", "w")
    else:
        hotkey_press("ctrl", "shift", "w")


def full_screen():
    """
    Toggle full screen mode.
    """
    if get_os() == "osx":
        hotkey_press("command", "shift", "f")
    else:
        press("f11")


def maximize_window():
    """
    Maximize the browser window to fill the screen
    This is NOT Full Screen mode
    """
    if get_os() == "osx":
        # There is no keybpard shortcut for this on Mac. We'll do it the old fashioned way.
        # This image is of the three window control buttons at top left of the window.
        window_controls = "window_maximize.png"

        # Alt key changes maximize button from full screen to maximize window.
        keyDown('alt')
        click(window_controls)
        keyUp('alt')

    elif get_os() == "win":
        type(text=Key.UP, modifier=KeyModifier.WIN)
        hotkey_press('win', 'up')
    else:
        # This is the documented method for window maximize,
        # but isn't working on one Linux config for unknown reasons,
        hotkey_press('win', 'ctrl', 'up')


def minimize_window():
    """
    Minimize the browser window to the application launch bar
    """
    if get_os() == "osx":
        hotkey_press("command", "m")
    else:
        hotkey_press("win", "down")


def new_tab():
    """
    Open a new browser tab.
    """
    if get_os() == "osx":
        hotkey_press('command', 't')
    else:
        type(text="t", modifier=KeyModifier.CTRL)
        hotkey_press('ctrl', 't')


def new_window():
    """
    Open a new browser window.
    """
    if get_os() == "osx":
        hotkey_press("command", "n")
    else:
        hotkey_press("ctrl", "n")


def new_private_window():
    """
    Open a new private browser window.
    """
    if get_os() == "osx":
        hotkey_press("command", "shift", "p")
    else:
        hotkey_press("ctrl", "shift", "p")


def next_tab():
    """
    Focus the next tab (one over to the right).
    """
    hotkey_press("ctrl", "tab")


def previous_tab():
    """
    Focus the previous tab (one over to the left).
    """
    hotkey_press("ctrl", "shift", "tab")


def quit_firefox():
    """
    Quit the browser.
    """
    if get_os() == "osx":
        hotkey_press('command', 'q')
    elif get_os() == "win":
        type(text="q", modifier=KeyModifier.CTRL + KeyModifier.SHIFT)
        hotkey_press('ctrl', 'shift', 'q')
    else:
        hotkey_press('ctrl', 'd')


def select_tab(num):
    """
    Select a given tab (only 1-8).
    param:  num  is a string 1-8. example: '4'.
    """
    if get_os() == "osx":
        hotkey_press("command", num)
    elif get_os() == "win":
        hotkey_press("ctrl", "shift", num)
    else:
        hotkey_press("ctrl", num)


def select_last_tab():
    """
    Select the last tab.
    """
    if get_os() == "osx":
        hotkey_press("command", 9)
    elif get_os() == "win":
        hotkey_press("ctrl", "shift", 9)
    else:
        hotkey_press("ctrl", 9)


def toggle_audio():
    """
    Mute/Unmute audio.
    """
    hotkey_press("ctrl", "m")


def undo_close_tab():
    """
    Re-opens the previously closed tab.
    """
    if get_os() == "osx":
        hotkey_press("command", "shift", "t")
    else:
        hotkey_press("ctrl", "shift", "t")


def undo_close_window():
    """
    Re-opens the previously closed browser window.
    """
    if get_os() == "osx":
        hotkey_press("command", "shift", "n")
    else:
        hotkey_press("ctrl", "shift", "n")


# End of Windows & Tabs keyboard shortcuts.

# Keyboard shortcuts for History & Bookmarks.

def history_sidebar():
    """
    Toggle open/close the history sidebar.
    """
    if get_os() == "osx":
        hotkey_press('command', 'shift', 'h')
    else:
        hotkey_press('ctrl', 'shift', 'h')


def clear_recent_history():
    """
    Open the Clear Recent History dialog.
    """
    if get_os() == "osx":
        hotkey_press('command', 'shift', 'delete')
    else:
        hotkey_press('ctrl', 'shift', 'delete')


def bookmark_all_tabs():
    """
    Open the Bookmark All Tabs dialog.
    """
    if get_os() == "osx":
        hotkey_press('command', 'shift', 'd')
    else:
        hotkey_press('ctrl', 'shift', 'd')


def bookmark_page():
    """
    Bookmark the current page.
    """
    if get_os() == "osx":
        hotkey_press('command', 'd')
    else:
        hotkey_press('ctrl', 'd')


def bookmarks_sidebar():
    """
    Toggle open/close the bookmarks sidebar.
    """
    if get_os() == "osx":
        hotkey_press('command', 'b')
    else:
        hotkey_press('ctrl', 'b')


def open_library():
    """
    Open the Library window.
    """
    if get_os() == "osx":
        hotkey_press("command", "shift", "b")
    else:
        hotkey_press("ctrl", "shift", "b")


# End History & Bookmarks keyboard shortcuts.

# Keyboard shortcuts for Tools.

def open_addons():
    """
    Open the Add-ons Manager page.
    """
    if get_os() == "osx":
        hotkey_press("command", "shift", "a")
    else:
        hotkey_press("ctrl", "shift", "a")


def open_downloads():
    """
    Open the Downloads dialog.
    """
    if get_os() == "osx":
        hotkey_press('command', 'j')
    elif get_os() == "win":
        hotkey_press('control', 'j')
    else:
        hotkey_press('control', 'y')


def open_page_source():
    """
    Open the current page's page source
    """
    if get_os() == "osx":
        hotkey_press('command', 'u')
    else:
        hotkey_press('ctrl', 'u')

# End Tools keyboard shortcuts
