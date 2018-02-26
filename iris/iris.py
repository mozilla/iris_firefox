# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import sys
import test_runner


class Iris(object):

    def __init__(self):
        print "iris.py: This is our main app"

        """
        Things to do here:
            * argument parsing
            * download and install Firefox
            * set up logging
        """
        print ' '.join(sys.argv[1:])
        test_runner.run(self)


Iris()
