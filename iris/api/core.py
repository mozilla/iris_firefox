# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


# This class is used to wrap methods around the Sikuli API

import os
from platform import *


def get_os():
    if os.path.exists("C:\\"):
        return "win"
    if os.path.exists("/Applications"):
        return "osx"
    else:
        return "linux"


def get_platform():
    if get_os() == "osx":
        return "osx"
    if sys.maxsize == 2 ** 31:
        return get_os() + "32"
    else:
        return get_os()


def get_module_dir():
    return os.path.realpath(os.path.split(__file__)[0] + "/../..")
