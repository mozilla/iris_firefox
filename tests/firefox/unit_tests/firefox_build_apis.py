# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='This is a unit test to verify basic Firefox build info.'
    )
    def run(self, firefox):
        assert firefox.application.version == get_firefox_version_from_about_config(), \
            'API for Firefox version is correct'
        assert firefox.application.build_id == get_firefox_build_id_from_about_config(), \
            'API for Firefox build ID is correct'
        assert firefox.application.channel == get_firefox_channel_from_about_config(), \
            'API for Firefox channel is correct'
        assert firefox.application.locale == get_firefox_locale_from_about_config(), \
            'API for Firefox locale is correct'

        assert firefox.application.version in get_support_info()['application']['version'], \
            'API for Firefox version is correct'
        assert firefox.application.build_id == get_support_info()['application']['buildID'], \
            'API for Firefox build ID is correct'
        assert firefox.application.channel == get_support_info()['application']['updateChannel'], \
            'API for Firefox channel is correct'
        assert firefox.application.locale == get_support_info()['intl']['localeService']['defaultLocale'], \
            'API for Firefox locale is correct'

        assert firefox.application.version == FirefoxUtils.get_firefox_version(firefox.application.path), \
            'API for Firefox version is correct'
        assert firefox.application.build_id == FirefoxUtils.get_firefox_build_id(firefox.application.path), \
            'API for Firefox build ID is correct'
        assert firefox.application.channel == FirefoxUtils.get_firefox_channel(firefox.application.path), \
            'API for Firefox channel is correct'
