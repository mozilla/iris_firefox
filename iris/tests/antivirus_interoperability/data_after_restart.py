# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = "No data loss after forced restart"
        self.test_case_id = "217874"
        self.test_suite_id = "3036"
        self.locale = ["en-US"]

    def run(self):
        cnn_page_downloaded_pattern = Pattern('cnn_page_downloaded.png')

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)

        soap_wiki_opened = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, soap_wiki_opened, 'SOAP Wiki site successfully opened')

        navigate('https://edition.cnn.com')

        cnn_page_opened = exists(cnn_page_downloaded_pattern, DEFAULT_HEAVY_SITE_LOAD_TIMEOUT)
        assert_true(self, cnn_page_opened, 'The CNN site successfully opened')

        close_content_blocking_pop_up()

        history_sidebar()
        click(Library.HISTORY_TODAY)

        time.sleep(5)
