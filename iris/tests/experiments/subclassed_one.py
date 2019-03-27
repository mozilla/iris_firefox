# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

# Rename the imported Test class to avoid a conflict with this class.
from basic_url import Test as BasicUrl

# Make sure to import everything that the BaseTest class has.
from iris.test_case import *


class Test(BasicUrl):

    def __init__(self):
        # As always, call the superclass constructor first.
        BasicUrl.__init__(self)
        self.meta = "This is a subclassed test from basic_url"
        self.enabled = False

    def setup(self):
        # As above, call the superclass constructor.
        BasicUrl.setup(self)

        # This test wants to use a private window on startup.
        self.private_window = True

    def run(self):
        # If you wiash to repeat the superclass test steps, call its run
        # method here.
        BasicUrl.run(self)

        # Subclassed test logic goes here.
        self.test_vars()
        navigate(self.new_test_url)
        expected = exists(self.amazon_image, 10)
        assert_true(self, expected, 'Wait for Amazon image to appear')

    def test_vars(self):
        self.new_test_url = 'https://www.amazon.com'
        self.amazon_image = Pattern('amazon.png')
        self.amazon_history_image = Pattern('amazon_history.png')
