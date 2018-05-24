# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test that checks for an existing bookmark in a custom profile'

    def setup(self):
        """ Test case setup
        This overrides the setup method in the BaseTest class,
        so that it can use a profile that already has bookmarks.
        """
        self.profile = Profile.TEN_BOOKMARKS
        launch_firefox(path=self.app.fx_path, profile=self.profile, url='about:blank')
        return

    def run(self):
        amazon_bookmark_image_1 = 'amazon_bookmark_1.png'
        amazon_bookmark_image_2 = 'amazon_bookmark_2.png'

        # Look for new bookmark via library menu button
        click('library.png')
        time.sleep(1)
        type(Key.TAB)
        type(Key.ENTER)
        time.sleep(1)

        expected_1 = exists(amazon_bookmark_image_1, 10)
        assert_true(self, expected_1, 'Find Amazon bookmark 1st image')

        type(Key.ESC)

        # Look for bookmark in bookmark menu
        bookmarks_sidebar()
        time.sleep(1)
        paste('amazon')
        time.sleep(1)

        expected_2 = exists(amazon_bookmark_image_2, 10, .7)
        assert_true(self, expected_2, 'Find Amazon bookmark 2nd image')
