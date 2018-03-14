# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import shutil
import subprocess

from api.core import *
from api.helpers.keyboard_shortcuts import *
from logger.iris_logger import *


add_image_path(os.path.join(os.path.split(__file__)[0], "images", get_os()))
logger = getLogger(__name__)


def launch_firefox(path, profile='empty_profile', url=None):
    # launch the app with optional args for profile, windows, URI, etc.
    current_dir = os.path.split(__file__)[0]
    active_profile = os.path.join(current_dir, "test_profiles", profile)
    if not os.path.exists (active_profile):
        os.mkdir(active_profile)

    cmd = [path]
    cmd.append('-foreground')
    cmd.append('-profile')
    cmd.append(active_profile)

    # TBD: other Firefox flags

    if url is not None:
        cmd.append('-url')
        cmd.append(url)

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return


def clean_profiles():
    path = os.path.join (os.path.split(__file__)[0], "test_profiles")
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)


# waits for firefox to exist by waiting for the home button to be present
def confirm_firefox_launch():
    try:
        wait("home.png", 20)
    except:
        print "Can't launch Firefox - aborting test run."
        exit(1)


def confirm_firefox_quit():
    try:
        waitVanish("home.png", 10)
    except:
        print "Firefox still around - aborting test run."
        exit(1)


def get_firefox_region():
    # TODO: needs better logic to determine bounds
    # For now, just return the whole screen
    return get_screen()


# navigates, via the location bar, to a given URL
#
# @param  url    the string to type into the location bar. The function
#                   handles typing "Enter" to complete the action.
#
def navigate(url):
    select_location_bar()
    # increase the delay between each keystroke while typing strings
    # (sikuli defaults to .02 sec)
    Settings.TypeDelay = 0.1
    type(url + Key.ENTER)


def restart_firefox(args):
    # just as it says, with options
    return


def get_menu_modifier():
    if get_os() == "osx":
        menu_modifier = Key.CTRL
    else:
        menu_modifier = Key.CMD
    return menu_modifier


def get_main_modifier():
    if get_os() == "osx":
        main_modifier = Key.CMD
    else:
        main_modifier = Key.CTRL
    return main_modifier


def copy_to_clipboard():
    edit_select_all()
    edit_copy()
    value=Env.getClipboard().strip()
    return value


def change_preference(pref_name,value):
    if exists("accept_risk.png",5):
        click("accept_risk.png")

    type(pref_name)
    time.sleep(2)
    type(Key.TAB)
    time.sleep(2)

    retrieved_value = None
    try:
        retrieved_value = copy_to_clipboard().split(";"[0])[1]
    except:
        logger.error("Failed to retrieve preference value")
        return None

    if retrieved_value == value:
        logger.debug("Flag is already set to value:" + value)
        return None
    else:
        # Typing enter here will toggle a boolean value
        type(Key.ENTER)
        # For non-boolean values, a dialog box should appear
        dialog_box = Pattern("preference_dialog_icon.png")
        if exists(dialog_box,3):
            type(dialog_box,value)
            type(Key.ENTER)

def reset_mouse():
    hover(Location(0, 0))
