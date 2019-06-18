# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='"The Swish Life" is properly loaded and works as intended',
        locale=['en-US'],
        test_case_id='125532',
        test_suite_id='2074',
    )
    def run(self, firefox):
        the_swish_life_tab_pattern = Pattern('the_swish_life_tab.png')
        fashion_tag_pattern = Pattern('fashion_tag.png')
        fashion_page_pattern = Pattern('fashion_page.png').similar(.7)
        the_home_button_pattern = Pattern('the_home_button.png')

        navigate('http://theswishlife.com/')

        window_opened = exists(the_swish_life_tab_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert window_opened is True, 'The Swish Life home page opened'

        page_end()

        fashion_tag_exists = exists(fashion_tag_pattern)
        if not fashion_tag_exists:
            assert fashion_tag_exists is False, 'The "Fashion" tag exists'

        click(fashion_tag_pattern)

        fashion_page_opened = exists(fashion_page_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert fashion_page_opened is True, 'The "Fashion" page is opened'

        click(the_home_button_pattern)

        home_page_label = exists(fashion_page_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert home_page_label is True, 'Return to the Swish Life home page. The website and the browser are stable'

