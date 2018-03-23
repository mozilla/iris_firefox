# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import os
import subprocess
import sys


# This is the main entry point defined in setup.py

def main(argv=None):
    # Required for Linux window communication
    os.environ["DISPLAY"] = ":99"

    # Get the project directory
    module_dir = os.path.split(__file__)[0]
    init_path = os.path.join(module_dir, "iris.py")

    cmd = ['python', init_path]
    args = sys.argv[1:]
    if len(args):
        for arg in args:
            cmd.append(arg)

    subprocess.Popen(cmd).communicate()


def detect_os():
    platform = None
    if sys.platform.startswith("darwin"):
        platform = "osx"
    elif sys.platform.startswith("linux"):
        platform = "linux"
    elif sys.platform.startswith("win"):
        platform = "win"
    return platform
