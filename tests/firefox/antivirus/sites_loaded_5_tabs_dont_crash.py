# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Multiple Alexa top sites loaded in 5 tabs don\'t crash.',
        locale=['en-US'],
        test_case_id='217877',
        test_suite_id='3063'
    )
    def run(self, firefox):
        youtube_logo_pattern = Pattern('youtube_logo.png')
        google_logo_pattern = Pattern('google_logo.png')
        blogspot_logo_pattern = Pattern('blogspot_logo.png')

        navigate(LocalWeb.SOAP_WIKI_TEST_SITE)
        assert exists(LocalWeb.SOAP_WIKI_SOAP_LABEL, 10), 'Wikipedia is properly loaded, no display issues.'

        new_tab()
        navigate('https://www.youtube.com/')
        assert exists(youtube_logo_pattern, Settings.DEFAULT_SITE_LOAD_TIMEOUT), \
            'YouTube is properly loaded in new tab, no display issues.'

        new_tab()
        navigate('https://www.google.com/')
        assert exists(google_logo_pattern, Settings.DEFAULT_SITE_LOAD_TIMEOUT), \
            'Google is properly loaded in new tab, no display issues.'

        new_tab()
        navigate('www.blogger.com/')
        assert exists(blogspot_logo_pattern, Settings.DEFAULT_SITE_LOAD_TIMEOUT), \
            'Blogspot is properly loaded in new tab, no display issues.'

        new_tab()
        navigate('https://edition.cnn.com/')
        assert exists(LocalWeb.CNN_LOGO, Settings. DEFAULT_HEAVY_SITE_LOAD_TIMEOUT), \
            'CNN is properly loaded in new tab, no display issues.'
