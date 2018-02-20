# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from api.core import *

# This helper defines keyboard shortcuts for many common actions in Firefox usage.
# We should be using these keyboard shortcuts whenever possible.


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


def select_location_bar():
    if get_os() == "osx":
        type(text="l", modifier=KeyModifier.CMD)
    else:
        type(text="l", modifier=KeyModifier.CTRL)
    # wait a little bit to allow location bar to become responsive
    sleep(0.5)


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
    if get_os() == "osx":
        type(text=Key.ESC)
    else:
        type(text=Key.ESC)
    # is this right? both actions are the same


def open_file_picker():
    if get_os() == "osx":
        type(text="o", modifier=KeyModifier.CMD)
    else:
        type(text="o", modifier=KeyModifier.CTRL)


def quit_firefox():
    if get_os() == "osx":
        type(text="q", modifier=Key.CMD)
    elif get_os() == "win":
        type(text="q", modifier=Key.CTRL+Key.SHIFT)
    else:
        type(text="q", modifier=Key.CTRL)


def new_tab():
    if get_os() == "osx":
        type(text="t", modifier=Key.CMD)
    else:
        type(text="t", modifier=Key.CTRL)


def new_window():
    if get_os() == "osx":
        type(text="n", modifier=Key.CMD)
    else:
        type(text="n", modifier=Key.CTRL)


def close_window():
    if get_os() == "osx":
        type(text="w", modifier=Key.CMD)
    else:
        type(text="w", modifier=Key.CTRL+Key.SHIFT)
