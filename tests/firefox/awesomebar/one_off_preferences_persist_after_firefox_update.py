# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='This test case checks that the one-off search feature does not affect the search engine '
                    'preferences after updating the Firefox version.',
        locale=['en-US'],
        test_case_id="108269",
        test_suite_id="1902",
        blocked_by={'id': '1488708', 'platform': OSPlatform.ALL},
        preferences={'app.update.auto': True,
                             'app.update.interval': 7200,
                             'app.update.badgeWaitTime': 10,
                             'app.update.lastUpdateTime.background-update-timer': 1,
                             'app.update.promptWaitTime': 30,
                             'app.update.timerMinimumDelay': 10}
    )
    def run(self, firefox):
        about_preferences_search_page_pattern = Pattern('about_preferences_search_page.png')
        default_search_engine_dropdown_pattern = Pattern('default_search_engine_dropdown.png')
        moz_search_amazon_search_engine_pattern = Pattern('moz_search_amazon_search_engine.png')
        find_more_search_engines_pattern = Pattern('find_more_search_engines.png')
        add_startpage_https_privacy_search_engine_pattern = Pattern('add_startpage_https_privacy_search_engine.png')
        add_to_firefox_pattern = Pattern('add_to_firefox.png')
        add_button_pattern = Pattern('add_button.png')
        startpage_https_search_engine_pattern = Pattern('startpage_https_search_engine.png')
        search_engine_pattern = Pattern('search_engine.png')
        google_one_off_button_pattern = Pattern('google_one_off_button.png')

        navigate(LocalWeb.FIREFOX_TEST_SITE)

        expected = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert expected, 'Page successfully loaded, firefox logo found.'

        new_tab()
        navigate('about:preferences#search')

        expected = exists(about_preferences_search_page_pattern, 10)
        assert expected, 'The \'about:preferences#search\' page successfully loaded.'

        expected = exists(default_search_engine_dropdown_pattern, 10)
        assert expected, 'Default search engine dropdown found.'

        click(default_search_engine_dropdown_pattern)

        # Change the default search engine.
        for i in range(2):
            type(Key.DOWN)

        type(Key.ENTER)

        # Check that default search engine successfully changed.
        previous_tab()

        select_location_bar()
        type(Key.DELETE)
        paste('moz')

        expected = exists(moz_search_amazon_search_engine_pattern, 10)
        assert expected, 'Default search engine successfully changed.'

        # Remove the 'Google' search engine.
        next_tab()

        for i in range(4):
            type(Key.TAB)

        if OSHelper.is_windows() or OSHelper.is_linux():
            type(Key.SPACE)

            expected = exists(search_engine_pattern, 10)
            assert expected, 'One-Click Search Engines section found.'
        else:
            search_engine_custom_pattern = Pattern('search_engine_61.0b9.png')
            type(Key.TAB)
            click(search_engine_custom_pattern.target_offset(20, 150))

            expected = exists(search_engine_custom_pattern, 10)
            assert expected, 'One-Click Search Engines section found.'

        # Check that unchecked search engine is successfully removed from the one-off searches bar.
        previous_tab()

        select_location_bar()
        type(Key.DELETE)
        paste('moz')

        if OSHelper.is_windows() or OSHelper.is_linux():
            try:
                expected = wait_vanish(google_one_off_button_pattern, 10)
                assert expected, 'Unchecked search engine successfully removed from the one-off searches'' bar.'
            except FindError:
                raise FindError('Unchecked search engine not removed from the one-off searches bar.')
        else:
            expected = exists(google_one_off_button_pattern.similar(0.9), 10)
            assert expected, 'Unchecked search engine successfully removed from the one-off searches bar.'

        # Add a new search engine.
        next_tab()

        # Tab 12 times to move focus at the bottom of the page so the search engine list is fully visible.
        for i in range(12):
            type(Key.TAB)

        type(Key.DOWN)

        expected = exists(find_more_search_engines_pattern, 10)
        assert expected, '\'Find more search engines\' link found.'

        click(find_more_search_engines_pattern)
        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)

        expected = exists(add_startpage_https_privacy_search_engine_pattern, 10)
        assert expected, '\'Start page HTTPS Privacy Search Engine\' engine successfully found.'

        click(add_startpage_https_privacy_search_engine_pattern)

        expected = exists(add_to_firefox_pattern, 10)
        assert expected, '\'Add to Firefox\' button found.'

        click(add_to_firefox_pattern)

        expected = exists(add_button_pattern, 10)
        assert expected, '\'Add\' button found.'

        click(add_button_pattern)

        previous_tab()

        expected = exists(startpage_https_search_engine_pattern, 10)
        assert expected, 'The search engine added found in the \'One-Click Search Engines\' section.'

        update_restart_pattern = Pattern('background_update_menu_notification.png').similar(0.5)
        firefox_up_to_date_pattern = Pattern('firefox_up_to_date.png')

        current_version = firefox.application.version
        channel = firefox.application.channel
        rules_dict = get_rule_for_channel(channel, current_version)

        assert rules_dict is not None, 'No rules found for {} channel. Please update config.ini file.'.format(channel)

        starting_condition = rules_dict['starting_condition']
        update_steps_list = rules_dict['steps'].split(',')

        assert current_version in FirefoxUtils.get_firefox_version(firefox.application.path), \
            'Firefox version is correct'

        if is_update_required(current_version, starting_condition):
            for update_step in update_steps_list:
                logger.info('Current version: %s, updating to version: %s.' % (current_version, update_step))

                open_about_firefox()
                wait(update_restart_pattern, 200)
                type(Key.ESC)
                firefox.restart()
                navigate(self.base_local_web_url)

                assert update_step in FirefoxUtils.get_firefox_version(firefox.application.path), \
                    'Firefox successfully updated'

                current_version = update_step

        open_about_firefox()
        wait(firefox_up_to_date_pattern, 20)
        type(Key.ESC)
        assert current_version in FirefoxUtils.get_firefox_version(firefox.application.path), \
            'Firefox version is correct'

        select_location_bar()
        paste('moz')

        expected = exists(moz_search_amazon_search_engine_pattern, 10)
        assert expected, 'The default search engine persist after Firefox version update.'

        if OSHelper.is_windows() or OSHelper.is_linux():
            try:
                expected = wait_vanish(google_one_off_button_pattern, 10)
                assert expected, 'The removed search engine from the one-off searches bar in previous Firefox ' \
                                 'version is still removed in the latest Firefox version.'
            except FindError:
                raise FindError('The removed search engine from the one-off searches bar in previous Firefox version '
                                'is not removed in the latest Firefox version.')
        else:
            expected = exists(google_one_off_button_pattern.similar(0.9), 10)
            assert not expected, 'The removed search engine from the one-off searches bar in previous Firefox ' \
                                 'version is still removed in the latest Firefox version.'

        navigate('about:preferences#search')

        # Tab 12 times to move focus at the bottom of the page so the search engine list is fully visible.
        for i in range(12):
            type(Key.TAB)

        expected = exists(startpage_https_search_engine_pattern, 10)
        assert expected, 'The new search engine added in previous Firefox version found in the ' \
                         '\'One-Click Search Engines\' section in the latest Firefox version.'
