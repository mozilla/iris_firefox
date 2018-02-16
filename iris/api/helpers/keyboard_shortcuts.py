# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from api.core import *
from api.helpers.general import *
import os

# This helper defines keyboard shortcuts for many common actions in Firefox usage.
# We should be using these keyboard shortcuts whenever possible.

# Get the operating system so we use the correct key combinations
op_sys = os.environ["OS_NAME"]

# Navigates back in browsing history one page visit
def navigate_back():
    if op_sys == "osx":
        type(text="[", modifier=KeyModifier.CMD)
    else:
        type(text="{", modifier=KeyModifier.ALT)


# Navigates forward in browsing history one page visit
def navigate_forward():
    if op_sys == "osx":
        type(text="]", modifier=KeyModifier.CMD)
    else:
        type(text="]", modifier=KeyModifier.ALT)


# Navigates the browser to whatever is set as the Home page
def navigate_home():
    type(text=Key.HOME, modifier=KeyModifier.ALT)


# Selects the location bar
def select_location_bar():
    if op_sys == "osx":
        type(text="l", modifier=KeyModifier.CMD)
    else:
        type(text="l", modifier=KeyModifier.CTRL)
    # wait a little bit to allow location bar to become responsive
    sleep(0.5)


# Reload the current web page
def reload_page():
    if op_sys == "osx":
        type(text="r", mmodifier=KeyModifier.CMD)
    else:
        type(text="r", modifier=KeyModifier.CTRL)


# Reload the current web page with cache override
def force_reload_page():
    if op_sys == "osx":
        type(text="r", modifier=KeyModifier.CMD + KeyModifier.SHIFT)
    else:
        type(text="r", modifier=KeyModifier.CTRL + KeyModifier.SHIFT)


# Stop the current in progress web page from loading
def stop_page_load():
    if op_sys == "osx":
        type(text=Key.ESC)
    else:
        type(text=Key.ESC)


# Open the file picker
def open_file_picker():
    if op_sys == "osx":
        type(text="o", modifier=KeyModifier.CMD)
    else:
        type(text="o", modifier=KeyModifier.CTRL)