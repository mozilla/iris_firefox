# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import subprocess

from api.core import *



def do_something():
    return "I am a helper function: " + str (get_key())


def launch_firefox(profile='empty_profile', url=None):
    # launch the app with optional args for profile, windows, URI, etc.
    current_dir = os.path.split(__file__)[0]
    active_profile = os.path.join(current_dir, "test_profiles", profile)


    # TEMP: hard-coding app path until we implement dynamic Fx installation
    if get_os() == "osx":
        path = '/Applications/Firefox.app/Contents/MacOS/firefox'
    elif get_os() == "win":
        path = 'C:\\Program Files (x86)\\Mozilla Firefox\\firefox.exe'
    else:
        # linux TBD
        path = ''

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
    if get_os() == "osx" or get_os() == "linux":
        cmd = ['rm', '-rf', path]
    else:
        cmd = ['rmdir', path, '/s']
    p = subprocess.Popen(cmd)
    return


def new_tab():
    type(text=Key.F2, modifier=get_menu_modifier())
    type(text="File")
    type(text=Key.DOWN)
    type(text="t", modifier=get_main_modifier())
    type(text=Key.UP)


def new_window():
    type(text=Key.F2, modifier=get_menu_modifier())
    type(text="File")
    type(text=Key.DOWN)
    type(text="n", modifier=get_main_modifier())
    type(text=Key.UP)


def close_window():
    type(text=Key.F2, modifier=get_menu_modifier())
    type(text="File")
    type(text=Key.DOWN)
    #close()
    get_screen().type("w", Key.SHIFT, get_main_modifier())
    type(text=Key.UP)


def restart_firefox(args):
    # just as it says, with options
    return


def quit_firefox():
    # just as it says, with options
    type(text=Key.F2, modifier=get_menu_modifier())
    type(text="Firefox")
    type(text="q", modifier=get_main_modifier())
    return

def get_menu_modifier():
    if get_os() == "osx":
        menu_modifier = Key.CTRL
    else:
        menu_modifier = Key.CTRL
    return menu_modifier


def get_main_modifier():
    if get_os() == "osx":
        main_modifier = Key.CMD
    else:
        main_modifier = Key.CMD
    return main_modifier


def get_os():
    return os.environ["OS_NAME"]


def get_platform():
    return os.environ["PLATFORM_NAME"]
