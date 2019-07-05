# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='This test case checks that more search engines can be added and are well displayed on one-off '
                    'searches bar.',
        locale=['en-US'],
        test_case_id='108261',
        test_suite_id='1902'
    )
    def run(self, firefox):
        moz_pattern = Pattern('moz.png')
        search_engine_pattern = Pattern('search_engine.png')
        search_settings_pattern = Pattern('search_settings.png')
        amazon_one_off_button_pattern = Pattern('amazon_one_off_button.png')
        bing_one_off_button_pattern = Pattern('bing_one_off_button.png')
        duck_duck_go_one_off_button_pattern = Pattern('duck_duck_go_one_off_button.png')
        google_one_off_button_pattern = Pattern('google_one_off_button.png')
        twitter_one_off_button_pattern = Pattern('twitter_one_off_button.png')
        wikipedia_one_off_button_pattern = Pattern('wikipedia_one_off_button.png')
        default_search_engine_dropdown_pattern = Pattern('default_search_engine_dropdown.png')
        moz_search_amazon_search_engine_pattern = Pattern('moz_search_amazon_search_engine.png')
        add_startpage_https_privacy_search_engine_pattern = Pattern('add_startpage_https_privacy_search_engine.png')
        find_more_search_engines_pattern = Pattern('find_more_search_engines.png')
        add_to_firefox_pattern = Pattern('add_to_firefox.png')
        add_button_pattern = Pattern('add_button.png')
        startpage_https_search_engine_pattern = Pattern('startpage_https_search_engine.png')
        startpage_one_off_button_pattern = Pattern('startpage_one_off_button.png')
        find_add_ons = Pattern('find_add_ons.png')
        google_one_click_search_pattern = Pattern('google_one_click_search.png')

        region = Region(0, 0, Screen().width, 2 * Screen().height / 3)

        navigate(LocalWeb.FIREFOX_TEST_SITE)

        test_site_opened = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert test_site_opened, 'Page successfully loaded, firefox logo found.'

        select_location_bar()
        paste('moz')

        pattern_list = [moz_pattern, search_settings_pattern, amazon_one_off_button_pattern,
                        bing_one_off_button_pattern, duck_duck_go_one_off_button_pattern, google_one_off_button_pattern,
                        twitter_one_off_button_pattern, wikipedia_one_off_button_pattern]

        # Deleted assert for ebay because we no longer have the ebay search engine in some locations.

        # Check that the default one-off list is displayed in the awesomebar.
        for index, pattern in enumerate(pattern_list):
            if OSHelper.is_mac():
                element_found = region.exists(pattern.similar(0.7), FirefoxSettings.FIREFOX_TIMEOUT)
                assert element_found, 'Element found at position {} in the list found.'.format(index)
            else:
                element_found = region.exists(pattern.similar(0.8), FirefoxSettings.FIREFOX_TIMEOUT)
                assert element_found, 'Element found at position {} in the list found.'.format(index)

        click(search_settings_pattern)

        pref_page_opened = exists(AboutPreferences.ABOUT_PREFERENCE_SEARCH_PAGE_PATTERN.similar(.6),
                                  FirefoxSettings.FIREFOX_TIMEOUT)
        assert pref_page_opened, 'The \'about:preferences#search\' page successfully loaded.'

        dropdown_found = exists(default_search_engine_dropdown_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert dropdown_found, 'Default search engine dropdown found.'

        click(default_search_engine_dropdown_pattern)

        # Change the default search engine.
        repeat_key_down(2)

        type(Key.ENTER)

        # Check that default search engine successfully changed.
        previous_tab()

        select_location_bar()
        type(Key.DELETE)
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT/2)
        paste('moz')
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT/2)
        type(Key.SPACE)

        search_engine_changed = exists(moz_search_amazon_search_engine_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert search_engine_changed, 'Default search engine successfully changed.'

        # Remove the 'Google' search engine.
        next_tab()

        open_find()

        type('One-click')

        one_click_section_found = exists(search_engine_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert one_click_section_found, 'One-Click Search Engines section found.'

        google_one_click_search_found = exists(google_one_click_search_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert google_one_click_search_found, 'Google One-Click Search Engines found.'

        google_width, google_height = google_one_click_search_pattern.get_size()

        click(google_one_click_search_pattern.target_offset(-google_width, 0))

        # Check that unchecked search engine is successfully removed from the one-off searches bar.
        previous_tab()

        select_location_bar()
        type(Key.DELETE)
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT/2)
        paste('moz')
        time.sleep(FirefoxSettings.TINY_FIREFOX_TIMEOUT/2)
        type(Key.SPACE)

        if OSHelper.is_windows() or OSHelper.is_linux():
            try:
                unchecked_engine_removed = wait_vanish(google_one_off_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
                assert unchecked_engine_removed, 'Unchecked search engine successfully removed from the one-off ' \
                                                 'searches bar.'
            except FindError:
                raise FindError('Unchecked search engine not removed from the one-off searches bar.')
        else:
            unchecked_engine_removed = exists(google_one_off_button_pattern.similar(0.9),
                                              FirefoxSettings.FIREFOX_TIMEOUT)
            assert not unchecked_engine_removed, 'Unchecked search engine successfully removed from the one-off ' \
                                                 'searches bar.'

        next_tab()

        pref_page_opened = exists(AboutPreferences.ABOUT_PREFERENCE_SEARCH_PAGE_PATTERN,
                                  FirefoxSettings.FIREFOX_TIMEOUT)
        assert pref_page_opened, 'The \'about:preferences#search\' page successfully loaded.'

        find_more_link_found = exists(find_more_search_engines_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert find_more_link_found, '\'Find more search engines\' link found.'

        click(find_more_search_engines_pattern)

        try:
            wait(find_add_ons, FirefoxSettings.FIREFOX_TIMEOUT)
            logger.debug('Find add-ons field is present on the page.')
            click(find_add_ons)
        except FindError:
            raise FindError('Find add-ons field is NOT present on the page, aborting.')

        paste('startpage')

        startpage_engine_found = exists(add_startpage_https_privacy_search_engine_pattern,
                                        FirefoxSettings.FIREFOX_TIMEOUT)
        assert startpage_engine_found, '\'Startpage HTTPS Privacy Search Engine\' engine successfully found.'

        click(add_startpage_https_privacy_search_engine_pattern)

        add_to_firefox_button_found= exists(add_to_firefox_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert add_to_firefox_button_found, '\'Add to Firefox\' button found.'

        click(add_to_firefox_pattern)

        add_button_found = exists(add_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert add_button_found, '\'Add\' button found.'

        click(add_button_pattern)

        previous_tab()

        startpage_engine_added = exists(startpage_https_search_engine_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert startpage_engine_added, 'The search engine added in the \'One-Click Search Engines\' section.'

        # Perform a new search in the url bar and make sure that everything looks ok after all the above changes.
        previous_tab()

        select_location_bar()
        type(Key.DELETE)
        paste('moz')
        type(Key.SPACE)

        dafault_engine_still_changed = exists(moz_search_amazon_search_engine_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert dafault_engine_still_changed, 'Default search engine is still changed.'

        new_engine_found = exists(startpage_one_off_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
        assert new_engine_found, 'Newly added search engine successfully found in the one-off searches bar.'

        if OSHelper.is_mac():
            unchecked_engine_still_removed = exists(google_one_off_button_pattern.similar(0.9),
                                                    FirefoxSettings.FIREFOX_TIMEOUT)
            assert not unchecked_engine_still_removed, 'Unchecked search engine is still removed from the one-off ' \
                                                       'searches bar.'
        else:
            unchecked_engine_still_removed = exists(google_one_off_button_pattern, FirefoxSettings.FIREFOX_TIMEOUT)
            assert not unchecked_engine_still_removed, 'Unchecked search engine is still removed from the one-off ' \
                                                       'searches bar.'
