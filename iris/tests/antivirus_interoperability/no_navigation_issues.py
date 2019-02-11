# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Alexa Top sites - no navigation issues'
        self.test_case_id = '217876'
        self.test_suite_id = '3063'
        self.locales = ['en-US']

    def run(self):
        blogspot_logo_pattern = Pattern('blogspot_logo.png')

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)
        wiki_soap_logo_exists = exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, DEFAULT_FIREFOX_TIMEOUT)
        assert_true(self, wiki_soap_logo_exists, 'Wikipedia is properly loaded, no display issues.')

        navigate('www.blogger.com/')
        blogspot_logo_exists = exists(blogspot_logo_pattern, DEFAULT_SITE_LOAD_TIMEOUT)
        assert_true(self, blogspot_logo_exists, 'Blogspot is properly loaded in new tab, no display issues.')

        navigate('https://edition.cnn.com/')
        cnn_logo_exists = exists(LocalWeb.CNN_LOGO, DEFAULT_HEAVY_SITE_LOAD_TIMEOUT)
        assert_true(self, cnn_logo_exists, 'CNN is properly loaded in new tab, no display issues.')

