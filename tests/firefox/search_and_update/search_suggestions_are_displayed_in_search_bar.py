# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Search suggestions are displayed by the field available on the about:newtab page.',
        locale=['en-US'],
        test_case_id='4268',
        test_suite_id='83',
    )
    def run(self, firefox):
        test_bold_pattern = Pattern('test_bold.png')
        test_search_bing_pattern = Pattern('test_search_bing.png')
        test_search_amazon_pattern = Pattern('test_search_amazon.png')
        test_search_duckduckgo_pattern = Pattern('test_search_duckduckgo.png')
        test_search_wikipedia_pattern = Pattern('test_search_wikipedia.png')
        bing_search_bar_pattern = Pattern('bing_search_bar.png')
        amazon_search_bar_pattern = Pattern('amazon_search_bar.png')
        duckduckgo_search_bar_pattern = Pattern('duckduckgo_search_bar.png').similar(0.6)
        wikipedia_search_bar_pattern = Pattern('wikipedia_search_bar.png').similar(0.6)

        one_click_engines_list = [bing_search_bar_pattern, amazon_search_bar_pattern, duckduckgo_search_bar_pattern,
                                  wikipedia_search_bar_pattern]

        test_search_list = [test_search_bing_pattern, test_search_amazon_pattern, test_search_duckduckgo_pattern,
                            test_search_wikipedia_pattern]

        change_preference('browser.search.widget.inNavBar', True)

        for i in range(one_click_engines_list.__len__()):
            select_search_bar()
            time.sleep(Settings.DEFAULT_UI_DELAY)

            if i == 0:
                paste('test')
                suggestions_shown = exists(test_bold_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
                assert suggestions_shown is True, 'Search suggestions are shown for the input in question.'

            search_engine = exists(one_click_engines_list[i], FirefoxSettings.FIREFOX_TIMEOUT)
            assert search_engine is True, 'The %s search engine is visible.' % \
                                          str(one_click_engines_list[i].get_filename()).split('_')[0].upper()

            click(one_click_engines_list[i])
            test_search = exists(test_search_list[i], FirefoxSettings.FIREFOX_TIMEOUT)

            assert test_search is True, 'Search results are displayed for the %s engine.' % \
                                        str(one_click_engines_list[i].get_filename()).split('_')[0].upper()
