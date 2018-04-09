# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from api.core import *


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
        type(text="[", modifier=KeyModifier.CMD)
    else:
        type(text=Key.LEFT, modifier=KeyModifier.ALT)


def navigate_forward():
    """
    Navigate forward in browsing history one page visit.
    """
    if get_os() == "osx":
        type(text="]", modifier=KeyModifier.CMD)
    else:
        type(text="]", modifier=KeyModifier.ALT)


def navigate_home():
    """
    Navigate the browser to whatever is set as the Home page.
    """
    type(text=Key.HOME, modifier=KeyModifier.ALT)


def open_file_picker():
    """
    Open the system file picker.
    """
    if get_os() == "osx":
        type(text="o", modifier=KeyModifier.CMD)
    else:
        type(text="o", modifier=KeyModifier.CTRL)


def select_location_bar():
    """
    Set focus to the locationbar.
    """
    if get_os() == "osx":
        type(text="l", modifier=KeyModifier.CMD)
    else:
        type(text="l", modifier=KeyModifier.CTRL)
    # wait to allow the location bar to become responsive.
    time.sleep(1)


def reload_page():
    """
    Reload the current web page.
    """
    if get_os() == "osx":
        type(text="r", modifier=KeyModifier.CMD)
    else:
        type(text="r", modifier=KeyModifier.CTRL)


def force_reload_page():
    """
    Reload the current web page with cache override.
    """
    if get_os() == "osx":
        type(text="r", modifier=KeyModifier.CMD + KeyModifier.SHIFT)
    else:
        type(text="r", modifier=KeyModifier.CTRL + KeyModifier.SHIFT)


def stop_page_load():
    """
    Stop the current in progress web page from loading.
    """
    type(text=Key.ESC)


# End of Navigation keyboard shortcuts.

# Keyboard shortcuts for Current Page.

def scroll_down():
    """
    Scroll down one increment (equivalant to 3 mousewheel steps).
    """
    type(text=Key.DOWN)


def scroll_up():
    """
    Scroll up one increment (equivalant to 3 mousewheel steps).
    """
    type(text=Key.UP)


def page_down():
    """
    Jump down one screen.
    """
    type(text=Key.SPACE)


def page_up():
    """
    Jump up one screen.
    """
    type(text=Key.SPACE, modifier=KeyModifier.SHIFT)


def page_end():
    """
    Jump to the bottom of the page.
    """
    type(text=Key.END)


def page_home():
    """
    Jump to the top of the page.
    """
    type(text=Key.HOME)


def focus_next_item():
    """
    Focus next actionable item.
    """
    type(text=Key.TAB)


def focus_previous_item():
    """
    Focus previous actionable item.
    """
    type(text=Key.TAB, modifier=KeyModifier.SHIFT)


def next_frame():
    """
    Move to the next frame (can be in content or in chrome).
    """
    type(text=Key.F6)


def previous_frame():
    """
    Move to the previous frame (can be in content or in chrome).
    """
    type(text=Key.F6, modifier=KeyModifier.SHIFT)


def open_print_page():
    """
    Open the Print dialog.
    """
    if get_os() == "osx":
        type(text="p", modifier=KeyModifier.CMD)
    else:
        type(text="p", modifier=KeyModifier.CTRL)


def open_save_page():
    """
    Open the Save dialog.
    """
    if get_os() == "osx":
        type(text="s", modifier=KeyModifier.CMD)
    else:
        type(text="s", modifier=KeyModifier.CTRL)


def zoom_in():
    """
    Zoom in one increment.
    """
    if get_os() == "osx":
        type(text="+", modifier=KeyModifier.CMD)
    else:
        type(text="+", modifier=KeyModifier.CTRL)


def zoom_out():
    """
    Zoom out one increment.
    """
    if get_os() == "osx":
        type(text="-", modifier=KeyModifier.CMD)
    else:
        type(text="-", modifier=KeyModifier.CTRL)


def restore_zoom():
    """
    Restores zoom level to page default.
    """
    if get_os() == "osx":
        type(text="0", modifier=KeyModifier.CMD)
    else:
        type(text="0", modifier=KeyModifier.CTRL)


# End of Current Page keyboard shortcuts.

# Keyboard shortcuts for Editing.

def edit_copy():
    """
    Copy selection to clipboard.
    """
    if get_os() == "osx":
        type(text="c", modifier=KeyModifier.CMD)
    else:
        type(text="c", modifier=KeyModifier.CTRL)


def edit_cut():
    """
    Cut selection to clipboard.
    """
    if get_os() == "osx":
        type(text="x", modifier=KeyModifier.CMD)
    else:
        type(text="x", modifier=KeyModifier.CTRL)


def edit_delete():
    """
    Delete selected text.
    If nothing is selected, delete previous character.
    """
    type(text=Key.DELETE)


def edit_paste():
    """
    Paste contents of the clipboard to the focused text field.
    """
    if get_os() == "osx":
        type(text="v", modifier=KeyModifier.CMD)
    else:
        type(text="v", modifier=KeyModifier.CTRL)


def edit_paste_plain():
    """
    Paste contents of the clipboard, as plain text, to the focused text field.
    """
    if get_os() == "osx":
        type(text="v", modifier=KeyModifier.CMD + KeyModifier.SHIFT)
    else:
        type(text="v", modifier=KeyModifier.CTRL + KeyModifier.SHIFT)


def edit_redo():
    """
    Redo the last operation of Undo.
    """
    if get_os() == "osx":
        type(text="z", modifier=KeyModifier.CMD + KeyModifier.SHIFT)
    else:
        type(text="z", modifier=KeyModifier.CTRL + KeyModifier.SHIFT)


def edit_select_all():
    """
    Selects the entire contents of focused field or page.
    """
    if get_os() == "osx":
        type(text="a", modifier=KeyModifier.CMD)
    else:
        type(text="a", modifier=KeyModifier.CTRL)


def edit_undo():
    """
    Undoes the previous operation.
    """
    if get_os() == "osx":
        type(text="z", modifier=KeyModifier.CMD)
    else:
        type(text="z", modifier=KeyModifier.CTRL)


# End of Editing keyboard shortcuts.

# Keyboard shortcuts for Search.

def open_find():
    """
    Open the find toolbar.
    """
    if get_os() == "osx":
        type(text="f", modifier=KeyModifier.CMD)
    else:
        type(text="f", modifier=KeyModifier.CTRL)


def find_next():
    """
    Find next occurance of term if find is already active on a search term.
    Find next (again) can also find the next occurance of a term without opening the find toolbar.
    """
    if get_os() == "osx":
        type(text="g", modifier=KeyModifier.CMD)
    else:
        type(text="g", modifier=KeyModifier.CTRL)


def find_previous():
    """
    Find the previous occurance of term, if find is already active on a search term.
    Find previous can also find the previous occurance of a term without opening the find toolbar.
    """
    if get_os() == "osx":
        type(text="g", modifier=KeyModifier.CMD + KeyModifier.SHIFT)
    else:
        type(text="g", modifier=KeyModifier.CTRL + KeyModifier.SHIFT)


def quick_find():
    """
    Quick find opens simple find toolbar that remains active for only six seconds.
    """
    if get_os() == "osx":
        type(text="/", modifier=KeyModifier.CMD)
    else:
        type(text="/", modifier=KeyModifier.CTRL)


def quick_find_link():
    """
    Quick find opens simple find link toolbar that remains active for only six seconds.
    """
    if get_os() == "osx":
        type(text="'", modifier=KeyModifier.CMD)
    else:
        type(text="'", modifier=KeyModifier.CTRL)


def close_find():
    """
    Close the regular find toolbar or quick find toolbar, if it has focus.
    """
    type(text=Key.ESC)


def select_search_bar():
    """
    If the search bar is present, select the search bar, otherwise this selects the location bar.
    """
    if get_os() == "osx":
        type(text="k", modifier=KeyModifier.CMD)
    else:
        type(text="k", modifier=KeyModifier.CTRL)


def change_search_next():
    """
    If the search bar has focus, change the search engine to the next in the list.
    (side effect: this also opens the search engine manager, if it wasn't alredy open).
    """
    if get_os() == "osx":
        type(text=Key.DOWN, modifier=KeyModifier.CMD)
    else:
        type(text=Key.DOWN, modifier=KeyModifier.CTRL)


def change_search_previous():
    """
    If the search bar has focus, change the search engine to the previous in the list.
    (side effect: this also opens the search engine manager, if it wasn't already open).
    """
    if get_os() == "osx":
        type(text=Key.UP, modifier=KeyModifier.CMD)
    else:
        type(text=Key.UP, modifier=KeyModifier.CTRL)


def open_search_manager():
    """
    If the search bar has focus open the search engine manager.
    """
    type(text=Key.DOWN, modifier=KeyModifier.ALT)


# End of Search keyboard shortcuts.


# Keyboard shortcuts for Windows & Tabs.

def close_tab():
    """
    Close the currently focused tab (Except for app tabs).
    """
    if get_os() == "osx":
        type(text="w", modifier=KeyModifier.CMD)
    else:
        type(text="w", modifier=KeyModifier.CTRL)


def close_window():
    """
    Close the currently focused window.
    """
    if get_os() == "osx":
        type(text="w", modifier=KeyModifier.CMD + KeyModifier.SHIFT)
    else:
        type(text="w", modifier=KeyModifier.CTRL + KeyModifier.SHIFT)


def full_screen():
    """
    Toggle full screen mode.
    """
    if get_os() == "osx":
        type(text="f", modifier=KeyModifier.CMD + KeyModifier.SHIFT)
    else:
        type(text=Key.F11)


def maximize_window():
    """
    Maximize the browser window to fill the screen
    This is NOT Full Screen mode
    """
    if get_os() == "osx":

        # temporarily disabling on Mac due to errors
        return
        # There is no keybpard shortcut for this on Mac. We'll do it the old fashioned way.
        # This image is of the three window control buttons at top left of the window.
        window_controls = "window_controls.png"

        # Set target to the maximize button
        maximize_button = Pattern(window_controls).targetOffset(21, 0)

        # We must hover the controls so the ALT key can take effect there.
        hover(image=window_controls)

        # Alt key changes maximize button from full screen to maximize window.
        keyDown(Key.ALT)
        click(maximize_button)
        keyUp(Key.ALT)

    elif get_os() == "win":
        type(text=Key.UP, modifier=KeyModifier.WIN)
    else:
        # This is the documented method for window maximize,
        # but isn't working on one Linux config for unknown reasons,
        type(text=Key.UP, modifier=KeyModifier.CTRL + KeyModifier.WIN)


def minimize_window():
    """
    Minimize the browser window to the application launch bar
    """
    if get_os() == "osx":
        type(text="m", modifier=Key.CMD)
    else:
        type(text=Key.DOWN, modifier=KeyModifier.WIN)


def new_tab():
    """
    Open a new browser tab.
    """
    if get_os() == "osx":
        type(text="t", modifier=KeyModifier.CMD)
    else:
        type(text="t", modifier=KeyModifier.CTRL)


def new_window():
    """
    Open a new browser window.
    """
    if get_os() == "osx":
        type(text="n", modifier=KeyModifier.CMD)
    else:
        type(text="n", modifier=KeyModifier.CTRL)


def new_private_window():
    """
    Open a new private browser window.
    """
    if get_os() == "osx":
        type(text="p", modifier=KeyModifier.CMD + KeyModifier.SHIFT)
    else:
        type(text="p", modifier=KeyModifier.CTRL + KeyModifier.SHIFT)


def next_tab():
    """
    Focus the next tab (one over to the right).
    """
    type(text=Key.TAB, modifier=KeyModifier.CTRL)


def previous_tab():
    """
    Focus the previous tab (one over to the left).
    """
    type(text=Key.TAB, modifier=KeyModifier.CTRL + KeyModifier.SHIFT)


def quit_firefox():
    """
    Quit the browser.
    """
    if get_os() == "osx":
        type(text="q", modifier=KeyModifier.CMD)
    elif get_os() == "win":
        type(text="q", modifier=KeyModifier.CTRL + KeyModifier.SHIFT)
    else:
        type(text="q", modifier=KeyModifier.CTRL)


def select_tab(num):
    """
    Select a given tab (only 1-8).
    param:  num  is a string 1-8. example: '4'.
    """
    if get_os() == "osx":
        type(text=num, modifier=KeyModifier.CMD)
    elif get_os() == "win":
        type(text=num, modifier=KeyModifier.CTRL + KeyModifier.SHIFT)
    else:
        type(text=num, modifier=KeyModifier.CTRL)


def select_last_tab():
    """
    Select the last tab.
    """
    if get_os() == "osx":
        type(text="9", modifier=KeyModifier.CMD)
    elif get_os() == "win":
        type(text="9", modifier=KeyModifier.CTRL + KeyModifier.SHIFT)
    else:
        type(text="9", modifier=KeyModifier.CTRL)


def toggle_audio():
    """
    Mute/Unmute audio.
    """
    type(text="m", modifier=KeyModifier.CTRL)


def undo_close_tab():
    """
    Re-opens the previously closed tab.
    """
    if get_os() == "osx":
        type(text="t", modifier=KeyModifier.CMD + KeyModifier.SHIFT)
    else:
        type(text="t", modifier=KeyModifier.CTRL + KeyModifier.SHIFT)


def undo_close_window():
    """
    Re-opens the previously closed browser window.
    """
    if get_os() == "osx":
        type(text="n", modifier=KeyModifier.CMD + KeyModifier.SHIFT)
    else:
        type(text="n", modifier=KeyModifier.CTRL + KeyModifier.SHIFT)


# End of Windows & Tabs keyboard shortcuts.

# Keyboard shortcuts for History & Bookmarks.

def history_sidebar():
    """
    Toggle open/close the history sidebar.
    """
    if get_os() == "osx":
        type(text="h", modifier=KeyModifier.CMD + KeyModifier.SHIFT)
    else:
        type(text="h", modifier=KeyModifier.CTRL)


def clear_recent_history():
    """
    Open the Clear Recent History dialog.
    """
    if get_os() == "osx":
        type(text=Key.DELETE, modifier=KeyModifier.CMD + KeyModifier.SHIFT)

        # Working around a pyautogui bug on Mac.
        # The key combination above causes the windows to disappear, i.e.:
        # pyautoguy.hotkey ("shift", "command", "delete")
        # Press the "fn" key twice to get back into the correct window state

        type(text=Key.FN)
        type(text=Key.FN)
    else:
        type(text=Key.DELETE, modifier=KeyModifier.CTRL + KeyModifier.SHIFT)


def bookmark_all_tabs():
    """
    Open the Bookmark All Tabs dialog.
    """
    if get_os() == "osx":
        type(text="d", modifier=KeyModifier.CMD + KeyModifier.SHIFT)
    else:
        type(text="d", modifier=KeyModifier.CTRL + KeyModifier.SHIFT)


def bookmark_page():
    """
    Bookmark the current page.
    """
    if get_os() == "osx":
        type(text="d", modifier=KeyModifier.CMD)
    else:
        type(text="d", modifier=KeyModifier.CTRL)


def bookmarks_sidebar():
    """
    Toggle open/close the bookmarks sidebar.
    """
    if get_os() == "osx":
        type(text="b", modifier=KeyModifier.CMD)
    else:
        type(text="b", modifier=KeyModifier.CTRL)


def open_library():
    """
    Open the Library window.
    """
    if get_os() == "osx":
        type(text="b", modifier=KeyModifier.CMD + KeyModifier.SHIFT)
    else:
        type(text="b", modifier=KeyModifier.CTRL + KeyModifier.SHIFT)


# End History & Bookmarks keyboard shortcuts.

# Keyboard shortcuts for Tools.

def open_addons():
    """
    Open the Add-ons Manager page.
    """
    if get_os() == "osx":
        type(text="a", modifier=KeyModifier.CMD + KeyModifier.SHIFT)
    else:
        type(text="a", modifier=KeyModifier.CTRL + KeyModifier.SHIFT)


def open_downloads():
    """
    Open the Downloads dialog.
    """
    if get_os() == "osx":
        type(text="j", modifier=KeyModifier.CMD)
    elif get_os() == "win":
        type(text="j", modifier=KeyModifier.CTRL)
    else:
        type(text="y", modifier=KeyModifier.CTRL)


def open_page_source():
    """
    Open the current page's page source
    """
    if get_os() == "osx":
        type(text="u", modifier=KeyModifier.CMD)
    else:
        type(text="u", modifier=KeyModifier.CTRL)


# End Tools keyboard shortcuts
