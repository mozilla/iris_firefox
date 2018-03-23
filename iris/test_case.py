# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import time

from api.core import *
from api.helpers.general import *
from api.helpers.keyboard_shortcuts import *
from logger.iris_logger import *
from configuration.config_parser import *

logger = getLogger(__name__)


class base_test(object):

    def __init__(self, app):
        self.app = app
        self.enable = True

    def _create_unique_profile_name(self):
        ts = int(time.time())
        profile_name = "profile_%s" % ts
        return profile_name

    def setup(self):
        """
        This might be a good place to declare variables or initialize Fx state.
        Also, by default, a new Firefox instance is created, with a blank profile and URL.
        If you wish to change this, override this method in your test case.
        """
        launch_firefox(path=self.app.fx_path, profile=self._create_unique_profile_name(), url="about:blank")
        return

    def resize_window(self):
        """
        By default, we will maximize the window.
        If this is not desired, override this method in your test case.
        """
        maximize_window()

    def run(self):
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
