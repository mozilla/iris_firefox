# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from api.core import *
from api.helpers.general import *
import os
import time


class base_test(object):

    def __init__(self, app):
        self._app = app


    def set_image_path(self, path):
        add_image_path(os.path.join(path, "images", self._app.os))


    def _create_unique_profile_name(self):
        ts = int(time.time())
        profile_name = "profile_%s" % ts
        return profile_name


    def setup (self):
        """
        This might be a good place to declare variables or initialize Fx state.
        Also, by default, a new Firefox instance is created, with a blank profile and URL.
        If you wish to change this, override this method in your test case.
        """
        launch_firefox(profile=self._create_unique_profile_name(), url="about:blank")
        return


    def run (self):
        """
        This is your test logic.
        """
        return


    def teardown(self):
        """
        This might be a good place to clean up what was done.
        """
        quit_firefox()
        return
