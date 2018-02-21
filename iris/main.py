# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import os
import subprocess
import sys


# This is the main entry point defined in setup.py

def main(argv=None):
    print "main.py: main"

    # Required for Linux window communication
    os.environ["DISPLAY"] = ":99"

    # Get the project directory
    module_dir = os.path.split(__file__)[0]

    # invoke the Sikuli jar in order to load our main app
    if detect_os() == "osx":
        jar_path = "/Applications/Sikuli/SikuliX.app/Contents/Java/sikulix.jar"
    elif detect_os() == "win":
        jar_path = "c:\Sikuli\sikulix.jar"
    else:
        temp = os.path.expanduser("~")
        jar_path = os.path.join(temp, "Sikuli/sikulix.jar")

    if not os.path.exists(jar_path):
        print "\nCan't find the Sikuli jar file. Terminating project now."
        print "Please consult the Iris wiki for information on setting up Sikuli"
        print "and its dependencies."
        print "https://github.com/mozilla/iris/wiki/Setup\n"
        exit (1)

    package = "org.python.util.jython"
    init_path = os.path.join(module_dir, "iris.py")

    cmd = ['java', '-cp', jar_path, package, init_path]

    # There is a problem at the moment invoking Firefox from jython, on Linux only
    # We will instruct Linux users on how to work around it in the meantime
    if detect_os() == "linux":
        print "Unable to launch iris on Linux via python due to outstanding issues."
        print "However, you can run iris via java instead."
        print "\tjava -cp %s %s %s" % (jar_path, package, init_path)
    else:
        p = subprocess.Popen(cmd).communicate()


def detect_os():
    platform = None
    if sys.platform.startswith("darwin"):
        platform = "osx"
    elif sys.platform.startswith("linux"):
        platform = "linux"
    elif sys.platform.startswith("win"):
        platform = "win"
    return platform
