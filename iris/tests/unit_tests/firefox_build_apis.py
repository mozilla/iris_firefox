# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This is a unit test to verify basic Firefox build info.'

    def run(self):
        # These asserts are for APIs that query the about:config preferences
        assert_equal(self, self.browser.version, get_firefox_version_from_about_config(),
                     'API for Firefox version is correct')
        assert_equal(self, self.browser.build_id, get_firefox_build_id_from_about_config(),
                     'API for Firefox build ID is correct')
        assert_equal(self, self.browser.channel, get_firefox_channel_from_about_config(),
                     'API for Firefox channel is correct')
        assert_equal(self, self.browser.locale, get_firefox_locale_from_about_config(),
                     'API for Firefox locale is correct')

        # These asserts are for APIs that query the about:support preferences
        assert_true(self, self.browser.version in get_support_info()['application']['version'],
                    'API for Firefox version is correct')
        assert_equal(self, self.browser.build_id, get_support_info()['application']['buildID'],
                     'API for Firefox build ID is correct')
        assert_equal(self, self.browser.channel, get_support_info()['application']['updateChannel'],
                     'API for Firefox channel is correct')
        assert_equal(self, self.browser.locale, get_support_info()['intl']['localeService']['defaultLocale'],
                     'API for Firefox locale is correct')

        # These asserts are for APIs that query the 'mozversion' module preferences
        assert_equal(self, self.browser.version, get_firefox_version(self.browser.path),
                     'API for Firefox version is correct')
        assert_equal(self, self.browser.build_id, get_firefox_build_id(self.browser.path),
                     'API for Firefox build ID is correct')
        assert_equal(self, self.browser.channel, get_firefox_channel(self.browser.path),
                     'API for Firefox channel is correct')
