# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import subprocess

from api.core import *



def do_something():
    return "I am a helper function: " + str (get_key())


def launch_firefox(profile='empty_profile', url=None, silent=None):
    # launch the app with optional args for profile, windows, URI, etc.
    current_dir = os.path.split(__file__)[0]
    active_profile = os.path.join(current_dir, "test_profiles", profile)

    # TEMP: hard-coding app path until we implement dynamic Fx installation
    path = '/Applications/Firefox.app/Contents/MacOS/firefox'
    cmd = [path]

    #if silent is not None:
    #    cmd.append('-silent')

    cmd.append('-foreground')
    cmd.append('-profile')
    cmd.append(active_profile)

    if url is not None:
        cmd.append('-url')
        cmd.append(url)

    #print cmd
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return


def clean_profiles():
    path = os.path.join (os.path.split(__file__)[0], "test_profiles")
    cmd = ['rm', '-rf', path]
    p = subprocess.Popen(cmd)
    return


def new_tab():
    type(text=Key.F2, modifier=Key.CTRL)
    type(text="File")
    type(text=Key.DOWN)
    type(text="t", modifier=Key.CMD)
    type(text=Key.UP)


def new_window():
    type(text=Key.F2, modifier=Key.CTRL)
    type(text="File")
    type(text=Key.DOWN)
    type(text="n", modifier=Key.CMD)
    type(text=Key.UP)


def close_window():
    type(text=Key.F2, modifier=Key.CTRL)
    type(text="File")
    type(text=Key.DOWN)
    close()
    #get_screen().type("w", Key.SHIFT, Key.CMD)
    type(text=Key.UP)


def restart_firefox(args):
    # just as it says, with options
    return


def quit_firefox():
    # just as it says, with options
    type(text=Key.F2, modifier=Key.CTRL)
    type(text="Firefox")
    type(text="q", modifier=Key.CMD)
    return


def get_os():
    return os.environ["OS_NAME"]


def get_platform():
    return os.environ["PLATFORM_NAME"]
