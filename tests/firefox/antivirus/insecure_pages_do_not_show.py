# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Check browser doesn\'t show insecure webpage errors',
        locale=['en-US'],
        test_case_id='225143',
        test_suite_id='3063'
    )
    def run(self, firefox):
        insecure_connection_pattern = Pattern('https_insecure_sign.png')
        twitter_logo_pattern = Pattern('twitter_logo.png')
        tracker_site_pattern = Pattern('firefox_download.png')

        change_preference('security.enterprise_roots.enabled', 'true')

        change_preference('security.enterprise_roots.enabled', 'false')

        navigate('https://www.twitter.com')
        close_content_blocking_pop_up()
        twitter_page_loaded = exists(twitter_logo_pattern, 10)
        assert twitter_page_loaded, 'Twitter webpage is loaded successfully'

        connection_insecure_not_displayed_twitter = not exists(insecure_connection_pattern, 10)
        assert connection_insecure_not_displayed_twitter, \
            'No error stating that the "connection is not secured" is displayed for twitter page'

        navigate('https://itisatrap.org/firefox/its-a-tracker.html')
        close_content_blocking_pop_up()
        tracker_site_loaded = exists(tracker_site_pattern, 10)
        assert tracker_site_loaded, '"It\'s a tracker" site loaded'

        connection_insecure_not_displayed_tracker_site = not exists(insecure_connection_pattern, 10)
        assert connection_insecure_not_displayed_tracker_site,\
            'No error stating that the "connection is not secured" is displayed for default tracker site'
