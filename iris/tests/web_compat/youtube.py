# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Web compatibility test for youtube.com'
        self.enabled = False

    def run(self):
        url = 'youtube.com'
        youtube_banner_pattern = Pattern('youtube_banner.png')
        youtube_filter_pattern = Pattern('filter_youtube_results.png')
        navigate(url)
        self.login_youtube()
        banner = exists(youtube_banner_pattern, 10)
        assert_true(self, banner, 'Youtube banner exists')
        logger.debug('Youtube Search')
        type('lord of the rings')
        type(Key.ENTER)
        filter_pattern = exists(youtube_filter_pattern, 10)
        assert_true(self, filter_pattern, 'Youtube filter exists')
        logger.debug('Results are displayed')
        time.sleep(3)
        type(Key.TAB)
        logger.debug('Scrolling down')
        for i in range(3):
            scroll_down()
            time.sleep(4)
        time.sleep(3)
        logger.debug('Scrolling up')
        for i in range(4):
            scroll_up()
        filter_pattern = exists(youtube_filter_pattern, 10)
        assert_true(self, filter_pattern, 'Youtube filter exists')

    def login_youtube(self):
        try:
            wait(Pattern('youtube_banner.png'), 10)
        except FindError:
            raise FindError('Can\'t find Youtube image in page, aborting test.')

        for i in range(5):
            type(Key.TAB)
        type(Key.ENTER)
        sign_in = exists(Pattern('youtube_sign_in.png'), 10)
        assert_true(self, sign_in, 'Youtube sign in exists')
        type(get_config_property('Youtube', 'username'))
        time.sleep(3)
        for i in range(2):
            type(Key.TAB)
        type(Key.ENTER)
        time.sleep(3)
        type(get_config_property('Youtube', 'password'))
        time.sleep(3)
        type(Key.TAB)
        type(Key.ENTER)
