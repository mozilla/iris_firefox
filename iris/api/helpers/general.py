# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import shutil
import subprocess

from api.core import *
from api.helpers.keyboard_shortcuts import *



def do_something():
    return "I am a helper function: " + str (get_key())


def launch_firefox(profile='empty_profile', url=None):
    # launch the app with optional args for profile, windows, URI, etc.
    current_dir = os.path.split(__file__)[0]
    active_profile = os.path.join(current_dir, "test_profiles", profile)
    if not os.path.exists (active_profile):
        os.mkdir(active_profile)

    # TEMP: hard-coding app path until we implement dynamic Fx installation
    if get_os() == "osx":
        path = '/Applications/Firefox.app/Contents/MacOS/firefox'
    elif get_os() == "win":
        path = 'C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe'
    else:
        path = '/usr/bin/firefox'

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
def firefox_exists():
    wait("home.png", 20)

    
# navigates, via the location bar, to a given URL
#
# @param  url    the string to type into the location bar. The function
#                   handles typing "Enter" to complete the action.
#
def navigate_to(url):
    #helper funcion from "keyboard_shotcuts"
    select_location_bar()
    # increase the delay between each keystroke while typing strings (sikuli defaults to .02 sec)
    Settings.TypeDelay = 0.1
    type(url + Key.ENTER)

    
def new_tab():
    if get_os() == "osx":
        # optional: force app focus
        #type(text=Key.F2, modifier=Key.CMD)
        type(text="t", modifier=Key.CMD)
    else:
        # optional: force app focus
        #click("menu.png")
        type(text="t", modifier=Key.CTRL)


def new_window():
    if get_os() == "osx":
        type(text=Key.F2, modifier=Key.CMD)
        type(text="n", modifier=Key.CMD)
    else:
        click("menu.png")
        type(text="n", modifier=Key.CTRL)


def close_window():
    if get_os() == "osx":
        type(text=Key.F2, modifier=Key.CMD)
        type(text="w", modifier=Key.CMD)
    else:
        click("menu.png")
        type(text="w", modifier=Key.CTRL+Key.SHIFT)


def restart_firefox(args):
    # just as it says, with options
    return


def quit_firefox():
    if get_os() == "osx":
        type(text=Key.F2, modifier=Key.CMD)
        type(text="q", modifier=Key.CMD)
    elif get_os() == "win":
        click("menu.png")
        type(text="q", modifier=Key.CTRL+Key.SHIFT)
    else:
        # don't force focus
        #click("menu.png")
        type(text="q", modifier=Key.CTRL)


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


def get_os():
    # working around a current Linux bug
    try:
        os_name = os.environ["OS_NAME"]
    except:
        os_name = "linux"
    return os_name


def get_platform():
    # working around a current Linux bug
    try:
        platform_name = os.environ["PLATFORM_NAME"]
    except:
        platform_name = "linux"
    return platform_name
