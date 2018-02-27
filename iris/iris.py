# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

import os
import sys
import test_runner
from logger.irisLogger import *

class Iris(object):

    def __init__(self):
        logger = getLogger(__name__)
        logger.info('This is our main app')

        """
        Things to do here:
            * argument parsing
            * download and install Firefox
            * set up logging
            * save data to 'self' object
        """

        # Checking for arguments
        if len (sys.argv[1]):
            print "args: %s" % ' '.join(sys.argv[1:])

        test_runner.run(self)


Iris()
