# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import os
import struct
import subprocess
import sys


# this is the main entry point defined in setup.py

def main(argv=None):
    print "main.py: main"

    # set up communication for headless mode
    os.environ["DISPLAY"] = ":99"

    # obtain OS information while we are still in actual Python
    # once we are in Java/Jython, these just return "Java"
    os.environ["OS_NAME"] = detect_os()
    os.environ["PLATFORM_NAME"] = detect_platform()

    module_dir = os.path.split(__file__)[0]

    # invoke the Sikuli jar in order to load a .sikuli package
    # which will in turn load our main app
    if detect_os() == "osx":
        jar_path = "/Applications/Sikuli/SikuliX.app/Contents/Java/sikulix.jar"
    elif detect_os() == "win":
        jar_path = "c:\Sikuli\sikulix.jar"
    else:
        jar_path = "~/Sikuli/sikulix.jar"


    package = "org.python.util.jython"
    init_path = os.path.join(module_dir, "app.py")


    cmd = ['java', '-cp', jar_path, package, init_path]
    p = subprocess.Popen(cmd).communicate()


def detect_platform():
    is_64bit = struct.calcsize('P') * 8 == 64
    platform = None
    if sys.platform.startswith("darwin"):
        platform = "osx"
    elif sys.platform.startswith("linux"):
        platform = "linux" if is_64bit else "linux32"
    elif sys.platform.startswith("win"):
        platform = "win" if is_64bit else "win32"
    return platform


def detect_os():
    # much like platform, only without processor info
    platform = None
    if sys.platform.startswith("darwin"):
        platform = "osx"
    elif sys.platform.startswith("linux"):
        platform = "linux"
    elif sys.platform.startswith("win"):
        platform = "win"
    return platform
