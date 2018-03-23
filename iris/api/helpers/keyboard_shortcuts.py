# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import time
from api.core import *
import pyautogui

pyautogui.FAILSAFE = False


# from logger.iris_logger import *

# logger = getLogger(__name__)

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

def typewrite(text, interval=0.02):
    print("Type: " + str(text))
    pyautogui.typewrite(text, interval)


def press(key):
    print("Press: " + key)
    pyautogui.keyDown(str(key))
    pyautogui.keyUp(str(key))


def navigate_back():
    """
    Navigate back in browsing history one page visit.
    """
    if get_os() == "osx":
        # @todo double check on mac
        pyautogui.hotkey('alt', 'left')
    else:
        pyautogui.hotkey('alt', 'left')


def navigate_forward():
    """
    Navigate forward in browsing history one page visit.
    """
    if get_os() == "osx":
        # @todo double check on mac
        pyautogui.hotkey('alt', 'right')
    else:
        pyautogui.hotkey('alt', 'right')


def navigate_home():
    """
    Navigate the browser to whatever is set as the Home page.
    """
    pyautogui.hotkey('alt', 'home')


def open_file_picker():
    """
    Open the system file picker.
    """
    if get_os() == "osx":
        pyautogui.hotkey('command', 'o')
    else:
        pyautogui.hotkey('ctrl', 'o')


def select_location_bar():
    """
    Set focus to the locationbar.
    """
    if get_os() == "osx":
        pyautogui.hotkey('command', 'l')
    else:
        pyautogui.hotkey('ctrl', 'l')
    # wait to allow the location bar to become responsive.
    time.sleep(1)


def reload_page():
    """
    Reload the current web page.
    """
    if get_os() == "osx":
        pyautogui.hotkey('command', 'r')
    else:
        pyautogui.hotkey('ctrl', 'r')


def force_reload_page():
    """
    Reload the current web page with cache override.
    """
    if get_os() == "osx":
        pyautogui.hotkey('command', 'shift', 'r')
    else:
        pyautogui.hotkey('ctrl', 'shift', 'r')


def stop_page_load():
    """
    Stop the current in progress web page from loading.
    """
    pyautogui.hotkey('escape')


# End of Navigation keyboard shortcuts.

# Keyboard shortcuts for Current Page.

def scroll_down(clicks=3):
    """
    Scroll down one increment (equivalant to 3 mousewheel steps).
    """
    pyautogui.scroll(clicks)


def scroll_up(clicks=-3):
    """
    Scroll up one increment (equivalant to 3 mousewheel steps).
    """
    pyautogui.scroll(clicks)


def page_down():
    """
    Jump down one screen.
    """
    pyautogui.press("space")


def page_up():
    """
    Jump up one screen.
    """
    pyautogui.hotkey('shift', 'space')


def page_end():
    """
    Jump to the bottom of the page.
    """
    pyautogui.press("end")


def page_home():
    """
    Jump to the top of the page.
    """
    pyautogui.press("home")


def focus_next_item():
    """
    Focus next actionable item.
    """
    pyautogui.press("tab")


def focus_previous_item():
    """
    Focus previous actionable item.
    """
    pyautogui.hotkey("shift", "tab")


def next_frame():
    """
    Move to the next frame (can be in content or in chrome).
    """
    pyautogui.press("f6")


def previous_frame():
    """
    Move to the previous frame (can be in content or in chrome).
    """
    pyautogui.hotkey("shift", 'f6')


def open_print_page():
    """
    Open the Print dialog.
    """
    if get_os() == "osx":
        pyautogui.hotkey("command", "p")
    else:
        pyautogui.hotkey("ctrl", "p")


def open_save_page():
    """
    Open the Save dialog.
    """
    if get_os() == "osx":
        pyautogui.hotkey("command", "s")
    else:
        pyautogui.hotkey("ctrl", "s")


def zoom_in():
    """
    Zoom in one increment.
    """
    if get_os() == "osx":
        pyautogui.hotkey("command", "+")
    else:
        pyautogui.hotkey("ctrl", "+")


def zoom_out():
    """
    Zoom out one increment.
    """
    if get_os() == "osx":
        pyautogui.hotkey("command", "-")
    else:
        pyautogui.hotkey("ctrl", "-")


def restore_zoom():
    """
    Restores zoom level to page default.
    """
    if get_os() == "osx":
        pyautogui.hotkey("command", "0")
    else:
        pyautogui.hotkey("ctrl", "0")


# End of Current Page keyboard shortcuts.

# Keyboard shortcuts for Editing.

def edit_copy():
    """
    Copy selection to clipboard.
    """
    if get_os() == "osx":
        pyautogui.hotkey("command", "c")
    else:
        pyautogui.hotkey("ctrl", "c")


def edit_cut():
    """
    Cut selection to clipboard.
    """
    if get_os() == "osx":
        pyautogui.hotkey("command", "x")
    else:
        pyautogui.hotkey("ctrl", "x")


def edit_delete():
    """
    Delete selected text.
    If nothing is selected, delete previous character.
    """
    pyautogui.press("delete")


def edit_paste():
    """
    Paste contents of the clipboard to the focused text field.
    """
    if get_os() == "osx":
        pyautogui.hotkey("command", "v")
    else:
        pyautogui.hotkey("ctrl", "v")


def edit_paste_plain():
    """
    Paste contents of the clipboard, as plain text, to the focused text field.
    """
    if get_os() == "osx":
        pyautogui.hotkey("command", "shift", "v")
    else:
        pyautogui.hotkey("ctrl", "shift", "v")


def edit_redo():
    """
    Redo the last operation of Undo.
    """
    if get_os() == "osx":
        pyautogui.hotkey("command", "shift", "z")
    else:
        pyautogui.hotkey("ctrl", "shift", "z")


def edit_select_all():
    """
    Selects the entire contents of focused field or page.
    """
    if get_os() == "osx":
        pyautogui.hotkey("command", "a")
    else:
        pyautogui.hotkey("ctrl", "a")


def edit_undo():
    """
    Undoes the previous operation.
    """
    if get_os() == "osx":
        pyautogui.hotkey("command", "z")
    else:
        pyautogui.hotkey("ctrl", "z")


# End of Editing keyboard shortcuts.

# Keyboard shortcuts for Search.

def open_find():
    """
    Open the find toolbar.
    """
    if get_os() == "osx":
        pyautogui.hotkey("command", "f")
    else:
        pyautogui.hotkey("ctrl", "f")


def find_next():
    """
    Find next occurance of term if find is already active on a search term.
    Find next (again) can also find the next occurance of a term without opening the find toolbar.
    """
    if get_os() == "osx":
        pyautogui.hotkey("command", "g")
    else:
        pyautogui.hotkey("ctrl", "g")


def find_previous():
    """
    Find the previous occurance of term, if find is already active on a search term.
    Find previous can also find the previous occurance of a term without opening the find toolbar.
    """
    if get_os() == "osx":
        pyautogui.hotkey("command", "shift", "g")
    else:
        pyautogui.hotkey("ctrl", "shift", "g")


def quick_find():
    """
    Quick find opens simple find toolbar that remains active for only six seconds.
    """
    if get_os() == "osx":
        pyautogui.hotkey("command", "/")
    else:
        pyautogui.hotkey("ctrl", "/")


def quick_find_link():
    """
    Quick find opens simple find link toolbar that remains active for only six seconds.
    """
    if get_os() == "osx":
        pyautogui.hotkey("command", "'")
    else:
        pyautogui.hotkey("ctrl", "'")


def close_find():
    """
    Close the regular find toolbar or quick find toolbar, if it has focus.
    """
    pyautogui.press("escape")


def select_search_bar():
    """
    If the search bar is present, select the search bar, otherwise this selects the location bar.
    """
    if get_os() == "osx":
        pyautogui.hotkey("command", "k")
    else:
        pyautogui.hotkey("ctrl", "k")


def change_search_next():
    """
    If the search bar has focus, change the search engine to the next in the list.
    (side effect: this also opens the search engine manager, if it wasn't alredy open).
    """
    if get_os() == "osx":
        pyautogui.hotkey("command", "down")
    else:
        pyautogui.hotkey("ctrl", "down")


def change_search_previous():
    """
    If the search bar has focus, change the search engine to the previous in the list.
    (side effect: this also opens the search engine manager, if it wasn't already open).
    """
    if get_os() == "osx":
        pyautogui.hotkey("command", "up")
    else:
        pyautogui.hotkey("ctrl", "up")


def open_search_manager():
    """
    If the search bar has focus open the search engine manager.
    """
    pyautogui.hotkey("alt", "down")


# End of Search keyboard shortcuts.


# Keyboard shortcuts for Windows & Tabs.

def close_tab():
    """
    Close the currently focused tab (Except for app tabs).
    """
    if get_os() == "osx":
        pyautogui.hotkey("command", "w")
    else:
        pyautogui.hotkey("ctrl", "w")


def close_window():
    """
    Close the currently focused window.
    """
    if get_os() == "osx":
        pyautogui.hotkey("command", "shift", "w")
    else:
        pyautogui.hotkey("ctrl", "shift", "w")


def full_screen():
    """
    Toggle full screen mode.
    """
    if get_os() == "osx":
        pyautogui.hotkey("command", "shift", "f")
    else:
        pyautogui.press("f11")


def maximize_window():
    """
    Maximize the browser window to fill the screen
    This is NOT Full Screen mode
    """
    if get_os() == "osx":
        # There is no keybpard shortcut for this on Mac. We'll do it the old fashioned way.
        # This image is of the three window control buttons at top left of the window.
        window_controls = "window_controls.png"

        # We must hover the controls so the ALT key can take effect there.
        hover(window_controls)

        # Alt key changes maximize button from full screen to maximize window.
        pyautogui.keyDown('alt')
        click(window_controls)
        pyautogui.keyUp('alt')

    elif get_os() == "win":
        pyautogui.hotkey('win', 'up')
    else:
        # This is the documented method for window maximize,
        # but isn't working on one Linux config for unknown reasons,
        pyautogui.hotkey('win', 'ctrl', 'up')


def minimize_window():
    """
    Minimize the browser window to the application launch bar
    """
    if get_os() == "osx":
        pyautogui.hotkey("command", "m")
    else:
        pyautogui.hotkey("win", "down")


def new_tab():
    """
    Open a new browser tab.
    """
    if get_os() == "osx":
        pyautogui.hotkey('command', 't')
    else:
        pyautogui.hotkey('ctrl', 't')


def new_window():
    """
    Open a new browser window.
    """
    if get_os() == "osx":
        pyautogui.hotkey("command", "n")
    else:
        pyautogui.hotkey("ctrl", "n")


def new_private_window():
    """
    Open a new private browser window.
    """
    if get_os() == "osx":
        pyautogui.hotkey("command", "shift", "p")
    else:
        pyautogui.hotkey("ctrl", "shift", "p")


def next_tab():
    """
    Focus the next tab (one over to the right).
    """
    pyautogui.hotkey("ctrl", "tab")


def previous_tab():
    """
    Focus the previous tab (one over to the left).
    """
    pyautogui.hotkey("ctrl", "shift", "tab")


def quit_firefox():
    """
    Quit the browser.
    """
    if get_os() == "osx":
        pyautogui.hotkey('command', 'q')
    elif get_os() == "win":
        pyautogui.hotkey('ctrl', 'shift', 'q')
    else:
        pyautogui.hotkey('ctrl', 'd')


def select_tab(num):
    """
    Select a given tab (only 1-8).
    param:  num  is a string 1-8. example: '4'.
    """
    if get_os() == "osx":
        pyautogui.hotkey("command", num)
    elif get_os() == "win":
        pyautogui.hotkey("ctrl", "shift", num)
    else:
        pyautogui.hotkey("ctrl", num)


def select_last_tab():
    """
    Select the last tab.
    """
    if get_os() == "osx":
        pyautogui.hotkey("command", 9)
    elif get_os() == "win":
        pyautogui.hotkey("ctrl", "shift", 9)
    else:
        pyautogui.hotkey("ctrl", 9)


def toggle_audio():
    """
    Mute/Unmute audio.
    """
    pyautogui.hotkey("ctrl", "m")


def undo_close_tab():
    """
    Re-opens the previously closed tab.
    """
    if get_os() == "osx":
        pyautogui.hotkey("command", "shift", "t")
    else:
        pyautogui.hotkey("ctrl", "shift", "t")


def undo_close_window():
    """
    Re-opens the previously closed browser window.
    """
    if get_os() == "osx":
        pyautogui.hotkey("command", "shift", "n")
    else:
        pyautogui.hotkey("ctrl", "shift", "n")


# End of Windows & Tabs keyboard shortcuts.

# Keyboard shortcuts for History & Bookmarks.

def history_sidebar():
    """
    Toggle open/close the history sidebar.
    """
    if get_os() == "osx":
        pyautogui.hotkey('command', 'shift', 'h')
    else:
        pyautogui.hotkey('ctrl', 'shift', 'h')


def clear_recent_history():
    """
    Open the Clear Recent History dialog.
    """
    if get_os() == "osx":
        pyautogui.hotkey('command', 'shift', 'delete')
    else:
        pyautogui.hotkey('ctrl', 'shift', 'delete')


def bookmark_all_tabs():
    """
    Open the Bookmark All Tabs dialog.
    """
    if get_os() == "osx":
        pyautogui.hotkey('command', 'shift', 'd')
    else:
        pyautogui.hotkey('ctrl', 'shift', 'd')


def bookmark_page():
    """
    Bookmark the current page.
    """
    if get_os() == "osx":
        pyautogui.hotkey('command', 'd')
    else:
        pyautogui.hotkey('ctrl', 'd')


def bookmarks_sidebar():
    """
    Toggle open/close the bookmarks sidebar.
    """
    if get_os() == "osx":
        pyautogui.hotkey('command', 'b')
    else:
        pyautogui.hotkey('ctrl', 'b')


def open_library():
    """
    Open the Library window.
    """
    if get_os() == "osx":
        pyautogui.hotkey("command", "shift", "b")
    else:
        pyautogui.hotkey("ctrl", "shift", "b")


# End History & Bookmarks keyboard shortcuts.

# Keyboard shortcuts for Tools.

def open_addons():
    """
    Open the Add-ons Manager page.
    """
    if get_os() == "osx":
        pyautogui.hotkey("command", "shift", "a")
    else:
        pyautogui.hotkey("ctrl", "shift", "a")


def open_downloads():
    """
    Open the Downloads dialog.
    """
    if get_os() == "osx":
        pyautogui.hotkey('command', 'j')
    elif get_os() == "win":
        pyautogui.hotkey('control', 'j')
    else:
        pyautogui.hotkey('control', 'y')


def open_page_source():
    """
    Open the current page's page source
    """
    if get_os() == "osx":
        pyautogui.hotkey('command', 'u')
    else:
        pyautogui.hotkey('ctrl', 'u')

# End Tools keyboard shortcuts
