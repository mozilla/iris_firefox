# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Removing search engines from preferences disabled \'Restore defaults\' button.'
        self.test_case_id = '111378'
        self.test_suite_id = '83'
        self.locale = ['en-US']

    def run(self):
        about_preferences_search_page_pattern = Pattern('about_preferences_search_page.png')
        wikipedia_search_bar_pattern = Pattern('wikipedia_search_bar.png')
        restore_default_search_engine_pattern = Pattern('restore_default_search_engine.png')
        remove_pattern = Pattern('remove.png')

        navigate('about:preferences#search')

        expected = exists(about_preferences_search_page_pattern, 10)
        assert_true(self, expected, 'The \'about:preferences#search\' page successfully loaded.')

        paste('one-click')

        expected = exists(wikipedia_search_bar_pattern, 10)
        assert_true(self, expected, 'The \'Wikipedia\' search engine is visible.')

        click(wikipedia_search_bar_pattern)

        try:
            wait(remove_pattern, 10)
            logger.debug('The \'Remove\' button is enabled.')
        except FindError:
            raise FindError('The \'Remove\' button is not enabled.')

        for i in range(3):
            click(remove_pattern)

        expected = exists(wikipedia_search_bar_pattern, 3)
        assert_false(self, expected, 'The \'Wikipedia\' search engine is removed.')

        try:
            wait(restore_default_search_engine_pattern, 10)
            logger.debug('The \'Restore Default Search Engines\' button is enabled.')
        except FindError:
            raise FindError('The \'Restore Default Search Engines\' button is not enabled.')

        click(restore_default_search_engine_pattern)

        expected = exists(wikipedia_search_bar_pattern, 10)
        assert_true(self, expected, 'The \'Wikipedia\' search engine is restored.')
