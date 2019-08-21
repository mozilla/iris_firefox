# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Firefox background browser update and default Search Code: Baidu.',
        locale=['zh-CN'],
        test_case_id='218337',
        test_suite_id='83',
        profile=Profiles.BRAND_NEW,
        preferences={'app.update.auto': True,
                     'app.update.interval': 7200,
                     'app.update.badgeWaitTime': 10,
                     'app.update.lastUpdateTime.background-update-timer': 1,
                     'app.update.promptWaitTime': 30,
                     'app.update.timerMinimumDelay': 10,
                     'browser.search.geoip.url': 'data:application/json,{\"country_code\": \"CN\"}',
                     'browser.search.region': 'CN'
                     },
        enabled=False
    )
    def run(self, firefox):
        url = LocalWeb.FOCUS_TEST_SITE
        default_search_engine_baidu_pattern = Pattern('default_search_engine_baidu.png')
        text_pattern = Pattern('focus_text.png')
        text_pattern_selected = Pattern('focus_text_selected.png')
        update_restart_pattern = Pattern('background_update_menu_notification.png')
        firefox_up_to_date_pattern = Pattern('firefox_up_to_date.png').similar(.7)
        version = firefox.application.version
        current_version = version if '-dev' not in version else version.replace('-dev', '')
        channel = firefox.application.channel
        rules_dict = get_rule_for_channel(channel, current_version)

        assert rules_dict is not None, 'No rules found for {} channel. Please update config.ini file.'.format(channel)

        starting_condition = rules_dict['starting_condition']
        update_steps_list = rules_dict['steps'].split(',')
        assert current_version in FirefoxUtils.get_firefox_version(firefox.application.path), \
            'Incorrect Firefox version.'

        restore_firefox_focus()
        change_preference('browser.search.widget.inNavBar', True)
        change_preference('browser.tabs.warnOnClose', True)

        navigate('about:preferences#search')
        expected = exists(default_search_engine_baidu_pattern, FirefoxSettings.FIREFOX_TIMEOUT,
                          region=Screen.MIDDLE_THIRD_HORIZONTAL)
        assert expected, 'Baidu is the default search engine prior to the browser update'

        # Perform a background browser update
        if is_update_required(current_version, starting_condition):
            for update_step in update_steps_list:

                if update_step == 'latest':
                    update_step = firefox.application.latest_version

                logger.info('Current version: %s, updating to version: %s.' % (current_version, update_step))

                try:
                    Mouse().move(Location(0, 0))
                    expected = exists(update_restart_pattern, 120)
                    assert expected, 'Restart for application update button found.'
                except FindError:
                    raise FindError('Background update hamburger menu icon notification did not appear, aborting.')

                firefox.restart()
                assert FirefoxUtils.get_firefox_version(firefox.application.path) in update_step, \
                    'Incorrect Firefox update.'
                current_version = FirefoxUtils.get_firefox_version(firefox.application.path)

        type(Key.ENTER)
        restore_firefox_focus()
        open_about_firefox()
        expected = exists(firefox_up_to_date_pattern, 20)
        assert expected, 'Firefox up to date message found.'
        type(Key.ESC)
        assert current_version in FirefoxUtils.get_firefox_version(firefox.application.path), \
            'Incorrect Firefox version.'

        new_tab()
        navigate(LocalWeb.MOZILLA_TEST_SITE)
        expected = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert expected, 'Background update sanity failed.'

        # Perform the Baidu default search engine code checks
        navigate('about:preferences#search')
        expected = exists(default_search_engine_baidu_pattern, FirefoxSettings.FIREFOX_TIMEOUT,
                          region=Screen.MIDDLE_THIRD_HORIZONTAL)
        assert expected, 'Baidu is the default search engine after the browser update.'

        # Perform a search using the awesome bar and then clear the content from it.
        select_location_bar()
        paste('test')
        type(Key.ENTER)
        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)
        select_location_bar()
        url_text = copy_to_clipboard()

        assert '/baidu?wd=test&tn=monline_7_dg' in url_text, 'The resulting URL contains the ' \
                                                             '\'monline_7_dg\' string.'

        select_location_bar()
        type(Key.DELETE)

        # Perform a search using the search bar.
        select_search_bar()
        paste('test')
        type(Key.ENTER)
        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)
        select_location_bar()
        url_text = copy_to_clipboard()

        assert '/baidu?wd=test&tn=monline_7_dg' in url_text, 'The resulting URL contains the ' \
                                                             '\'monline_7_dg\' string.'

        # Highlight some text and right click it.
        new_tab()
        navigate(url)
        expected = exists(text_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert expected, 'Page successfully loaded, focus text found.'

        double_click(text_pattern)
        time.sleep(Settings.DEFAULT_UI_DELAY_SHORT)
        right_click(text_pattern_selected)
        time.sleep(Settings.DEFAULT_UI_DELAY_SHORT)
        repeat_key_down(3)
        type(Key.ENTER)
        time.sleep(Settings.DEFAULT_UI_DELAY_LONG)
        select_location_bar()
        url_text = copy_to_clipboard()

        assert '/baidu?wd=Focus&tn=monline_7_dg' in url_text, 'The resulting URL contains the ' \
                                                              '\'monline_7_dg\' string.'
