# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='This test case checks that telemetry data is collected for one-offs from new tab',
        locale=['en-US'],
        test_case_id='108274',
        test_suite_id='1902'
    )
    def run(self, firefox):
        url = LocalWeb.FIREFOX_TEST_SITE
        bing_search_results_moz_pattern = Pattern('bing_search_results_moz.png')
        focus_on_search_bar = Pattern('focus_on_search_bar.png')

        navigate(url)
        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert expected, 'Page successfully loaded, firefox logo found.'

        new_tab()
        select_location_bar()

        try:
            wait(focus_on_search_bar, 5)
            logger.debug('Search Bar is present on the page.')
            click(focus_on_search_bar)
        except FindError:
            raise FindError('Search Bar is NOT present on the page, aborting.')

        paste('moz')

        # Wait a moment for the suggests list to fully populate before stepping down through it.
        time.sleep(Settings.DEFAULT_UI_DELAY)

        for i in range(7):
            type(Key.DOWN)
        type(Key.ENTER)

        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)

        expected = exists(bing_search_results_moz_pattern, 10)
        assert expected, 'Search results performed with \'Bing\' search engine.'

        info = get_telemetry_info()['payload']['stores']['main']['parent']['keyedHistograms']['SEARCH_COUNTS']

        assert str(info['bing.newtab']['range']) == '[1, 2]', 'Range is correct.'
        assert str(info['bing.newtab']['bucket_count']) == '3', 'Bucket count is correct.'
        assert str(info['bing.newtab']['histogram_type']) == '4', 'Histogram type is correct.'
        assert str(info['bing.newtab']['values']['1']) == '0', 'Values[1] is correct.'
        assert str(info['bing.newtab']['values']['0']) == '1', 'Values[0] is correct.'
        assert str(info['bing.newtab']['sum']), '1' == 'Sum is correct.'
