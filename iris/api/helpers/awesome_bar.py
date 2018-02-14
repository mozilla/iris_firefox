# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from api.core import *
import os


# this will set the image path for this module
current_dir = os.path.split(__file__)[0]
path = os.path.join(current_dir, "images")
add_image_path(path)


def navigate(url):
    wait("1516888289228.png", 10)
    type((Pattern("1516888289228.png").targetOffset(221, 0)), url + Key.ENTER)
    return


def back_in_history():
    wait("1517514241697.png", 5)
    click("1517514241697.png")
    return


def forward_in_history():
    wait("1517514418304.png", 5)
    click("1517514418304.png")
    return
