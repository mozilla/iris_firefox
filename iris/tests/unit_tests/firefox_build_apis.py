# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a unit test to verify basic Firefox build info.'

    def run(self):
        # These asserts are for APIs that query the about:config preferences
        assert_equal(self, self.app.version, get_firefox_version_from_about_support(),
                     'API for Firefox version is correct')
        assert_equal(self, self.app.build_id, get_firefox_build_id_from_about_support(),
                     'API for Firefox build ID is correct')
        assert_equal(self, self.app.fx_channel, get_firefox_channel_from_about_support(),
                     'API for Firefox channel is correct')
        assert_equal(self, self.app.fx_locale, get_firefox_locale_from_about_support(),
                     'API for Firefox locale is correct')

        # These asserts are for APIs that query the about:support preferences
        assert_equal(self, self.app.version, get_support_info()['application']['version'],
                     'API for Firefox version is correct')
        assert_equal(self, self.app.build_id, get_support_info()['application']['buildID'],
                     'API for Firefox build ID is correct')
        assert_equal(self, self.app.fx_channel, get_support_info()['application']['updateChannel'],
                     'API for Firefox channel is correct')
        assert_equal(self, self.app.fx_locale, get_support_info()['intl']['localeService']['defaultLocale'],
                     'API for Firefox locale is correct')

        # These asserts are for APIs that query the 'mozversion' module preferences
        assert_equal(self, self.app.version, get_firefox_version(self.app.fx_path),
                     'API for Firefox version is correct')
        assert_equal(self, self.app.build_id, get_firefox_build_id(self.app.fx_path),
                     'API for Firefox build ID is correct')
        assert_equal(self, self.app.fx_channel, get_firefox_channel(self.app.fx_path),
                     'API for Firefox channel is correct')
