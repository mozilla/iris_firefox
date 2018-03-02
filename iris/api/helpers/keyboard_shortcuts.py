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


########## Navigation ##########

# Navigates back in browsing history one page visit
def navigate_back():
    if get_os() == "osx":
        type(text="[", modifier=KeyModifier.CMD)
    else:
        type(text="{", modifier=KeyModifier.ALT)


# Navigates forward in browsing history one page visit
def navigate_forward():
    if get_os() == "osx":
        type(text="]", modifier=KeyModifier.CMD)
    else:
        type(text="]", modifier=KeyModifier.ALT)


# Navigates the browser to whatever is set as the Home page
def navigate_home():
    type(text=Key.HOME, modifier=KeyModifier.ALT)


# Opens the system file picker
def open_file_picker():
    if get_os() == "osx":
        type(text="o", modifier=KeyModifier.CMD)
    else:
        type(text="o", modifier=KeyModifier.CTRL)


# Set focus to the locationbar
def select_location_bar():
    if get_os() == "osx":
        type(text="l", modifier=KeyModifier.CMD)
    else:
        type(text="l", modifier=KeyModifier.CTRL)
    # wait a little bit to allow location bar to become responsive
    sleep(1)


# Reload the current web page
def reload_page():
    if get_os() == "osx":
        type(text="r", modifier=KeyModifier.CMD)
    else:
        type(text="r", modifier=KeyModifier.CTRL)


# Reload the current web page with cache override
def force_reload_page():
    if get_os() == "osx":
        type(text="r", modifier=KeyModifier.CMD + KeyModifier.SHIFT)
    else:
        type(text="r", modifier=KeyModifier.CTRL + KeyModifier.SHIFT)


# Stop the current in progress web page from loading
def stop_page_load():
    type(text=Key.ESC)


########## end Navigation ##########

########## Current Page ##########

# Scroll down one increment (equivilant to 3 mousewheel steps)
def scroll_down():
    type(text=Key.DOWN)


# Scroll up one increment (equivilant to 3 mousewheel steps)
def scroll_up():
    type(text=Key.UP)


# Jump down one screen
def page_down():
    type(text=Key.SPACE)


# Jump up one screen
def page_up():
    type(text=Key.SPACE, modifier=KeyModifier.SHIFT)


# Jump to the bottom of the page
def page_end():
    type(text=Key.END)


# Jump to the top of the page
def page_home():
    type(text=Key.HOME)


# Focus next actionable item
def focus_next_item():
    type(text=Key.TAB)


# Focus previous actionable item
def focus_previous_item():
    type(text=Key.TAB, modifier=KeyModifier.SHIFT)


# Move to the next frame (can be in content or in chrome)
def next_frame():
    type(text=Key.F6)


# Move to the previous frame (can be in content or in chrome)
def previous_frame():
    type(text=Key.F6, modifier=KeyModifier.SHIFT)


# Open the print dialog
def open_print_page():
    if get_os() == "osx":
        type(text="p", modifier=KeyModifier.CMD)
    else:
        type(text="p", modifier=KeyModifier.CTRL)


# Open the save dialog
def open_save_page():
    if get_os() == "osx":
        type(text="s", modifier=KeyModifier.CMD)
    else:
        type(text="s", modifier=KeyModifier.CTRL)


# Zoom in one increment
def zoom_in():
    if get_os() == "osx":
        type(text="+", modifier=KeyModifier.CMD)
    else:
        type(text="+", modifier=KeyModifier.CTRL)


# Zoom out one increment
def zoom_out():
    if get_os() == "osx":
        type(text="-", modifier=KeyModifier.CMD)
    else:
        type(text="-", modifier=KeyModifier.CTRL)


# Restores zoom level to page default
def restore_zoom():
    if get_os() == "osx":
        type(text="0", modifier=KeyModifier.CMD)
    else:
        type(text="0", modifier=KeyModifier.CTRL)


########## end Current Page ##########

########## Editing ##########

# Copy selection to clipboard
def edit_copy():
    if get_os() == "osx":
        type(text="c", modifier=KeyModifier.CMD)
    else:
        type(text="c", modifier=KeyModifier.CTRL)


# Cut selection to clipboard
def edit_cut():
    if get_os() == "osx":
        type(text="x", modifier=KeyModifier.CMD)
    else:
        type(text="x", modifier=KeyModifier.CTRL)


# Delete selection or if nothing is selected, delete previous character
def edit_delete():
    type(text=Key.DELETE)


# Paste contents of the clipboard to the focused text field
def edit_paste():
    if get_os() == "osx":
        type(text="v", modifier=KeyModifier.CMD)
    else:
        type(text="v", modifier=KeyModifier.CTRL)


# Paste contents of the clipboard, as plain text, to the focus text field
def edit_paste_plain():
    if get_os() == "osx":
        type(text="v", modifier=KeyModifier.CMD + KeyModifier.SHIFT)
    else:
        type(text="v", modifier=KeyModifier.CTRL + KeyModifier.SHIFT)


# Redo the last operation of Undo
def edit_redo():
    if get_os() == "osx":
        type(text="z", modifier=KeyModifier.CMD + KeyModifier.SHIFT)
    else:
        type(text="z", modifier=KeyModifier.CTRL + KeyModifier.SHIFT)


# Selects the entire contents of focused field or page
def edit_select_all():
    if get_os() == "osx":
        type(text="a", modifier=KeyModifier.CMD)
    else:
        type(text="a", modifier=KeyModifier.CTRL)


# Undoes the previous operation
def edit_undo():
    if get_os() == "osx":
        type(text="z", modifier=KeyModifier.CMD)
    else:
        type(text="z", modifier=KeyModifier.CTRL)


########## end Editing ##########

########## Search ##########

# Open the find toolbar
def open_find():
    if get_os() == "osx":
        type(text="f", modifier=KeyModifier.CMD)
    else:
        type(text="f", modifier=KeyModifier.CTRL)


# Find next occurance of term if find is already active on a search term
# Find next (again) can also find the next occurance of a term without opening the find toolbar
def find_next():
    if get_os() == "osx":
        type(text="g", modifier=KeyModifier.CMD)
    else:
        type(text="g", modifier=KeyModifier.CTRL)


# Find the previous occurance of term if find is already active on a search term
# Find previous can also find the next occurance of a term without opening the find toolbar
def find_previous():
    if get_os() == "osx":
        type(text="g", modifier=KeyModifier.CMD + KeyModifier.SHIFT)
    else:
        type(text="g", modifier=KeyModifier.CTRL + KeyModifier.SHIFT)


# Quick find opens simple find toolbar that remains active for only six seconds
def quick_find():
    if get_os() == "osx":
        type(text="/", modifier=KeyModifier.CMD)
    else:
        type(text="/", modifier=KeyModifier.CTRL)


# Quick find opens simple find link toolbar that remains active for only six seconds
def quick_find_link():
    if get_os() == "osx":
        type(text="'", modifier=KeyModifier.CMD)
    else:
        type(text="'", modifier=KeyModifier.CTRL)


# Close the regular find toolbar or quick find toolbar, if  it has focus
def close_find():
    type(text=Key.ESC)


# If the search bar is present, select the search bar, otherwise this selects the location bar
def select_search_bar():
    if get_os() == "osx":
        type(text="k", modifier=KeyModifier.CMD)
    else:
        type(text="k", modifier=KeyModifier.CTRL)


# If the search bar has focus change the search engine to the next in the list
# (side effect: this also opens the search engine manager, if it wasn't alredy open)
def change_search_next():
    if get_os() == "osx":
        type(text=Key.DOWN, modifier=KeyModifier.CMD)
    else:
        type(text=Key.DOWN, modifier=KeyModifier.CTRL)


# If the search bar has focus change the search engine to the prvious in the list
# (side effect: this also opens the search engine manager, if it wasn't alredy open)
def change_search_previous():
    if get_os() == "osx":
        type(text=Key.UP, modifier=KeyModifier.CMD)
    else:
        type(text=Key.UP, modifier=KeyModifier.CTRL)


# If the search bar has focus open the search engine manager
def open_search_manager():
    type(text=Key.DOWN, modifier=KeyModifier.ALT)


########## end Search ##########

########## Windows & Tabs ##########

# Close the currently focused tab (Except for app tabs)
def close_tab():
    if get_os() == "osx":
        type(text="w", modifier=KeyModifier.CMD)
    else:
        type(text="w", modifier=KeyModifier.CTRL)


# Close the currently focused window
def close_window():
    if get_os() == "osx":
        type(text="w", modifier=KeyModifier.CMD + KeyModifier.SHIFT)
    else:
        type(text="w", modifier=KeyModifier.CTRL + KeyModifier.SHIFT)


# Mute/Unmute audio
def toggle_audio():
    type(text="m", modifier=KeyModifier.CTRL)


# Open a new browser tab
def new_tab():
    if get_os() == "osx":
        type(text="t", modifier=KeyModifier.CMD)
    else:
        type(text="t", modifier=KeyModifier.CTRL)


# Open a new browser window
def new_window():
    if get_os() == "osx":
        type(text="n", modifier=KeyModifier.CMD)
    else:
        type(text="n", modifier=KeyModifier.CTRL)


# Open a new private browser window
def new_private_window():
    if get_os() == "osx":
        type(text="p", modifier=KeyModifier.CMD + KeyModifier.SHIFT)
    else:
        type(text="p", modifier=KeyModifier.CTRL + KeyModifier.SHIFT)


# Focus the next tab (one over to the right)
def next_tab():
    type(text=Key.TAB, modifier=KeyModifier.CTRL)


# Focus the previous tab (one over to the left)
def previous_tab():
    type(text=Key.TAB, modifier=KeyModifier.CTRL + KeyModifier.SHIFT)


# Quit the browser
def quit_firefox():
    if get_os() == "osx":
        type(text="q", modifier=KeyModifier.CMD)
    elif get_os() == "win":
        type(text="q", modifier=KeyModifier.CTRL + KeyModifier.SHIFT)
    else:
        type(text="q", modifier=KeyModifier.CTRL)


# Select a given tab (only 1-8)
# param:  num  is a string 1-8. example: "4"
def select_tab(num):
    if get_os() == "osx":
        type(text=num, modifier=KeyModifier.CMD)
    elif get_os() == "win":
        type(text=num, modifier=KeyModifier.CTRL + KeyModifier.SHIFT)
    else:
        type(text=num, modifier=KeyModifier.CTRL)


# Select the last tab
def select_last_tab():
    if get_os() == "osx":
        type(text="9", modifier=KeyModifier.CMD)
    elif get_os() == "win":
        type(text="9", modifier=KeyModifier.CTRL + KeyModifier.SHIFT)
    else:
        type(text="9", modifier=KeyModifier.CTRL)


# Re-opens the previously closed tab
def undo_close_tab():
    if get_os() == "osx":
        type(text="t", modifier=KeyModifier.CMD + KeyModifier.SHIFT)
    else:
        type(text="t", modifier=KeyModifier.CTRL + KeyModifier.SHIFT)


# Re-opens the previously closed browser window
def undo_close_window():
    if get_os() == "osx":
        type(text="n", modifier=KeyModifier.CMD + KeyModifier.SHIFT)
    else:
        type(text="n", modifier=KeyModifier.CTRL + KeyModifier.SHIFT)

########## end Windows & Tabs ##########