# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import test_runner

class App(object):

    def __init__(self):
        print "app.py: This is our main app"

        """
        Things to do here:
            * argument parsing
            * download and install Firefox
            * set up logging
        """
        self.platform = os.environ["PLATFORM_NAME"]
        self.os = os.environ["OS_NAME"]

        test_runner.run(self)


App()