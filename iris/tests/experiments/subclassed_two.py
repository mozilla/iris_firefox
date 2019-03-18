# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

# Rename the imported Test classes to avoid a conflict with this class.
from basic_url import Test as BasicUrl
from subclassed_one import Test as SubclassedOne

# Make sure to import everything that the BaseTest class has.
from iris.test_case import *


class Test(SubclassedOne):

    def __init__(self):
        # As always, call the superclass constructor first.
        SubclassedOne.__init__(self)
        self.meta = "This is a subclassed test from subclassed_one"
        self.enabled = False

    def setup(self):
        # As above, call the superclass constructor.
        SubclassedOne.setup(self)

        # This test wants to use a normal browsing window on startup,
        # unlike its superclass, which uses a private window.
        self.private_window = False

    def run(self):
        # This test does not wish to repeat its superclass test logic, so
        # it will not call its immediate superclass run method.
        # However, it still wants to run the logic from the topmost superclass,
        # which navigates to the Google search page. So, it calls that instead.
        BasicUrl.run(self)

        # New test logic goes here. The variables for the steps below come from calling a
        # method in the superclass called "test_vars". This is one way to share
        # data across tests via inheritance.
        self.test_vars()

        # We will confirm that we do not see the Amazon logo.
        expected = exists(self.amazon_image, 5)
        assert_false(self, expected, 'Amazon image is not present')

        # We can continue to write test logic thereafter.
        navigate(LocalWeb.FIREFOX_TEST_SITE)
        expected = exists(LocalWeb.FIREFOX_IMAGE, 5)
        assert_true(self, expected, 'Firefox image is present')
