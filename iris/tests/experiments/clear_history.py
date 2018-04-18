# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = "This is a test for clearing browser history"

    def run(self):
        url = "https://www.amazon.com"
        amazon_image = "amazon.png"
        amazon_history_image = "amazon_history.png"
        home_image = "home.png"

        navigate(url)

        expected_1 = wait(amazon_image)
        assert_true(self, expected_1, 'Wait for amazon image to appear')

        # The various calls to time.sleep are necessary to
        # account for lag times incurred by underlying operations.
        # We can always switch to image detection as a mechanism to
        # confirm presence of UI before interaction, but that
        # has its own cost.

        clear_recent_history()
        time.sleep(1)
        type(Key.ENTER)
        time.sleep(1)

        # The click here is required, because the Firefox window loses
        # focus after invoking the above dialog, and without it,
        # the keyboard shortcuts don't work

        click(home_image)

        # Navigate to new page; otherwise, our bitmap for the history item
        # looks identical to the image in the title bar and we'll get
        # a false match
        navigate("about:blank")

        history_sidebar()
        time.sleep(2)
        type("amazon")

        expected_2 = exists(amazon_history_image, 10)
        assert_true(self, expected_2, 'Find amazon history image')
