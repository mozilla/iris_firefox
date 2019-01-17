# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Scrolling works properly while being zoomed in or out.'
        self.test_case_id = '4659'
        self.test_suite_id = '102'
        self.locales = ['en-US']

    def run(self):
        after_zooming_in_content_pattern = Pattern('after_zooming_in_content.png')
        after_zooming_out_content_pattern = Pattern('after_zooming_out_content.png')

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)
        web_page_loaded_exists = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, web_page_loaded_exists, 'The website in question is properly loaded.')

        [zoom_in() for _ in range(2)]

        after_zooming_in_content_exists = exists(after_zooming_in_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, after_zooming_in_content_exists, 'Zoom in action works properly')

        [zoom_out() for _ in range(4)]

        after_zooming_out_content_exists = exists(after_zooming_out_content_pattern, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, after_zooming_out_content_exists, 'Zoom out action works properly')