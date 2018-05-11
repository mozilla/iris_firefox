# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'Web compability test for youtube.com'
        self.exclude = Platform.ALL

    def run(self):
        url = 'youtube.com'
        youtube_banner = 'youtube_banner.png'
        youtube_filter = 'filter_youtube_results.png'
        navigate(url)
        self.login_youtube()
        banner = exists(youtube_banner, 10)
        assert_true(self, banner, 'Youtube banner exists')
        logger.debug('Youtube Search')
        type('lord of the rings')
        type(Key.ENTER)
        filter = exists(youtube_filter, 10)
        assert_true(self, filter, 'Youtube filter exists')
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
        filter = exists(youtube_filter, 10)
        assert_true(self, filter, 'Youtube filter exists')

    def login_youtube(self):
        try:
            wait('youtube_banner.png', 10)
        except:
            logger.error('Can\'t find Youtube image in page, aborting test.')
            return

        for i in range(5):
            type(Key.TAB)
        type(Key.ENTER)
        sign_in = exists('youtube_sign_in.png', 10)
        assert_true(self, sign_in, 'Youtube sign in exists')
        type(get_credential('Youtube', 'username'))
        time.sleep(3)
        for i in range(2):
            type(Key.TAB)
        type(Key.ENTER)
        time.sleep(3)
        type(get_credential('Youtube', 'password'))
        time.sleep(3)
        type(Key.TAB)
        type(Key.ENTER)
