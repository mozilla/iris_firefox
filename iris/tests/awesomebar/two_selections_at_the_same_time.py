# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This test case perform 2 selections at the same time.'
        self.test_case_id = '108257'
        self.test_suite_id = '1902'

    def run(self):
        hover_duck_duck_go_one_off_button = Pattern('hover_duck_duck_go_one_off_button.png')
        duck_duck_go_one_off_button = Pattern('duck_duck_go_one_off_button.png')
        search_with_url_autocomplete = Pattern('search_with_url_autocomplete.png')
        twitter_one_off_button_highlight = Pattern('twitter_one_off_button_highlight.png')
        default_status = Pattern('default_status.png')
        modified_status = Pattern('modified_status.png')
        true_value = Pattern('true_value.png')
        false_value = Pattern('false_value.png')
        amazon_logo = Pattern('amazon_logo.png')
        accept_risk = Pattern('accept_risk.png')

        region = Region(0, 0, SCREEN_WIDTH, 2 * SCREEN_HEIGHT / 3)

        navigate('www.amazon.com')

        expected = exists(amazon_logo, 10)
        assert_true(self, expected, 'Page successfully loaded, amazon logo found.')

        navigate('about:config')

        click(accept_risk)

        expected = region.exists(default_status, 10)
        assert_true(self, expected, 'The \'about:config\' page successfully loaded and default status is correct.')

        paste('keyword.enabled')
        type(Key.ENTER)

        expected = region.exists(default_status, 10)
        assert_true(self, expected, 'The \'keyword.enabled\' preference has status \'default\' by default.')

        expected = region.exists(true_value, 10)
        assert_true(self, expected, 'The \'keyword.enabled\' preference has value \'true\' by default.')

        double_click(default_status)

        expected = region.exists(modified_status, 10)
        assert_true(self, expected,
                    'The \'keyword.enabled\' preference has status \'modified\' after the preference has changed.')

        expected = region.exists(false_value, 10)
        assert_true(self, expected,
                    'The \'keyword.enabled\' preference has value \'false\' after the preference has changed.')

        select_location_bar()
        paste('amaz')

        expected = region.exists(search_with_url_autocomplete, 10)
        assert_true(self, expected, 'Search is performed with url autocomplete for pages where you have been before.')

        hover(duck_duck_go_one_off_button)

        expected = exists(hover_duck_duck_go_one_off_button, 10)
        assert_true(self, expected, 'Mouse is over the \'DuckDuckGo\' search engine.')

        expected = region.exists(search_with_url_autocomplete, 10)
        assert_true(self, expected, 'The autocomplete is still displayed after user hovers an one-off button.')

        for i in range(15):
            scroll_down()

        expected = region.exists(twitter_one_off_button_highlight, 10)
        assert_true(self, expected, 'The \'Twitter\' one-off button is highlighted.')
