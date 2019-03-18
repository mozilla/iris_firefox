# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Web compatibility test for baidu.com'
        self.enabled = False

    def run(self):
        url = 'www.baidu.com'
        search_baidu = Pattern('baidu_home.png')
        search_item = 'Barack Obama'
        search_page_pattern = Pattern('baidu_search_page.png')

        logger.debug('Accessing ' + url + '...')
        navigate(url)

        expected_1 = exists(search_baidu, 10)
        assert_true(self, expected_1, 'Baidu search button should be visible')

        logger.debug(url + ' successfully loaded')

        type(search_item)
        type(Key.ENTER)
        logger.debug('Searching: %s' % search_item)

        search_confirmation = exists(search_page_pattern, 10)
        assert_true(self, search_confirmation, 'Search action should be finished')
