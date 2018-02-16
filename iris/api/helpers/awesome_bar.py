# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from api.core import *
from api.helpers.general import *
import os


# this will set the image path for this module
current_dir = os.path.split(__file__)[0]
path = os.path.join(current_dir, "images", get_os())
add_image_path(path)


# Navigates via the location bar to a given URL
def navigate_to(url):
    select_location_bar()
    slowType(url + Key.ENTER, 0.1)


def back_in_history():
    wait("back.png", 10)
    click("back.png")
    return


def forward_in_history():
    wait("forward.png", 10)
    click("forward.png")
    return