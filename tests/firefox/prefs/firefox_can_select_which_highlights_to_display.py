# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    # def setup(self):
    #     pass

    @pytest.mark.details(
        description='Firefox Home Content - Firefox can select which Highlights to display',
        test_case_id='161671',
        test_suite_id='2241',
        locale=['en-US'],
        preferences={'devtools.chrome.enabled': True}
        # profile=Profiles.Bookmarks_Downloads_Visited_Pockets
    )
    def run(self, firefox):
        about_preferences_home_url_pattern = Pattern('about_preferences_home_url.png')
        about_preferences_home_highlights_default = Pattern('about_preferences_home_highlights_default.png')
        options_displayed_in_the_highlight_section = Pattern('options_displayed_in_the_highlight_section.png')
        highlighted_sites_when_all_option_selected = Pattern('highlighted_sites_when_all_option_selected.png')
        github_logo = Pattern('github_logo.png')
        github_topbar_for_recent_page_test = Pattern('github_topbar_for_recent_page_test.png')
        download_history_button = Pattern('download_history_button.png')
        save_to_pocket_icon = Pattern('save_to_pocket_icon.png')
        page_saved_to_pocket = Pattern('page_saved_to_pocket.png')
        pocket_login_icon = Pattern('pocket_login_icon.png')
        pocket_login_confirmation = Pattern('pocket_login_confirmation.png')
        pocket_login_email = Pattern('pocket_login_email.png')
        pocket_login_loginbutton = Pattern('pocket_login_loginbutton.png')
        visited_page_checkbox = Pattern('visited_page_checkbox.png')
        bookmarks_checkbox = Pattern('bookmarks_checkbox.png')
        most_recent_download_checkbox = Pattern('most_recent_download_checkbox.png')
        pages_saved_to_pocket_checkbox = Pattern('pages_saved_to_pocket_checkbox.png')
        highlights_most_recent_download = Pattern('highlights_most_recent_download.png')
        highlights_bookmarks = Pattern('highlights_bookmarks.png')
        highlights_saved_page = Pattern('highlights_saved_page.png')
        highlights_page_saved_to_pocket = Pattern('highlights_page_saved_to_pocket.png')

        # Bookmark a website for Bookmark verification
        url = LocalWeb.FIREFOX_TEST_SITE
        bookmark_button_pattern = LocationBar.STAR_BUTTON_UNSTARRED
        navigate(url)
        expected = exists(LocalWeb.FIREFOX_LOGO, FirefoxSettings.FIREFOX_TIMEOUT)
        assert expected, 'Page could not be loaded as firefox logo not found.'
        select_location_bar()
        click(bookmark_button_pattern)
        type(Key.ENTER)

        # Open some website for Visited Page verification
        new_tab()
        navigate('https://github.com/mozilla/iris_firefox')
        wait(github_logo)
        click(github_logo)
        wait(github_topbar_for_recent_page_test, 10)

        # Save a web page to Pocket for pages saved to Pocket verification
        new_tab()
        navigate('https://www.mozilla.org/en-US/')
        click(save_to_pocket_icon)
        click(pocket_login_icon)

        wait(pocket_login_email, 20)
        type('test@qa.com')
        type(Key.TAB)
        type('test@qa')
        click(pocket_login_loginbutton)

        pocket_login_confirmation_exists = exists(pocket_login_confirmation, FirefoxSettings.FIREFOX_TIMEOUT)
        assert pocket_login_confirmation_exists, 'Pocket login could not succeeded.'

        previous_tab()
        click(save_to_pocket_icon)
        page_saved_to_pocket_exists = exists(page_saved_to_pocket, FirefoxSettings.FIREFOX_TIMEOUT)
        assert page_saved_to_pocket_exists, 'Page could not saved to pocket.'

        # Download a website for Most Recent Download verification
        firefox.restart()
        url = 'https://www.google.com/'
        new_tab()
        navigate(url)

        if OSHelper.is_mac():
            type(text='s', modifier=KeyModifier.CMD)
        else:
            type(text='s', modifier=KeyModifier.CTRL)
        time.sleep(Settings.DEFAULT_UI_DELAY)

        type(Key.ENTER)
        type(text='y', modifier=KeyModifier.ALT)
        wait(download_history_button)
        click(download_history_button)

        # Navigate to about:preferences#home -> Highlights
        new_tab()
        navigate('about:preferences#home')
        about_preferences_home_url_exists = exists(about_preferences_home_url_pattern,
                                                   FirefoxSettings.FIREFOX_TIMEOUT)
        assert about_preferences_home_url_exists, 'Home section of about:preferences page could not loaded successfully'

        click(AboutPreferences.FIND_IN_OPTIONS)
        paste('Highlights')

        # Highlight options selected by default
        about_preferences_home_highlights_default_exists = exists(about_preferences_home_highlights_default,
                                                                  FirefoxSettings.FIREFOX_TIMEOUT)
        assert about_preferences_home_highlights_default_exists, \
            'Checkbox option present in "Highlights" is not selected by default'

        # Options displayed in highlight section
        options_displayed_in_the_highlight_section_exists = exists(options_displayed_in_the_highlight_section,
                                                                   FirefoxSettings.FIREFOX_TIMEOUT)
        assert options_displayed_in_the_highlight_section_exists, \
            'Checkbox option is not present in "Highlights" for Visited Pages, Bookmarks, ' \
            'Most Recent Download and Pages Saved to Pocket'

        # New tab displayed when all four highlights options are selected
        new_tab()
        highlighted_sites_when_all_option_selected_exists = exists(highlighted_sites_when_all_option_selected,
                                                                   FirefoxSettings.FIREFOX_TIMEOUT)
        assert highlighted_sites_when_all_option_selected_exists, \
            'Visited Pages, Bookmarks, Most Recent Download and Pages Saved to Pocket are ' \
            'not displayed in Highlights section'

        # New tab displayed when only "Visited Pages" option is selected in highlights
        navigate('about:preferences#home')
        click(AboutPreferences.FIND_IN_OPTIONS)
        paste('Highlights')
        click(bookmarks_checkbox)
        click(most_recent_download_checkbox)
        click(pages_saved_to_pocket_checkbox)
        new_tab()
        highlights_most_recent_download_exists = exists(highlights_most_recent_download,
                                                        FirefoxSettings.FIREFOX_TIMEOUT)
        assert highlights_most_recent_download_exists, 'Most recent download page is not displayed in Highlights'

        # New tab displayed when only "Bookmarks" option is selected in highlights
        navigate('about:preferences#home')
        click(AboutPreferences.FIND_IN_OPTIONS)
        paste('Highlights')
        click(visited_page_checkbox)
        click(bookmarks_checkbox)
        new_tab()
        highlights_bookmarks_exists = exists(highlights_bookmarks, FirefoxSettings.FIREFOX_TIMEOUT)
        assert highlights_bookmarks_exists, 'Bookmarks page is not displayed in Highlights'

        # New tab displayed when only "Most Recent Download" option is selected in highlights
        navigate('about:preferences#home')
        click(AboutPreferences.FIND_IN_OPTIONS)
        paste('Highlights')
        click(bookmarks_checkbox)
        click(most_recent_download_checkbox)
        new_tab()
        highlights_saved_page_exists = exists(highlights_saved_page, FirefoxSettings.FIREFOX_TIMEOUT)
        assert highlights_saved_page_exists, 'Downloaded page or Saved page is not displayed in Highlights'

        # New tab displayed when only "Pages Saved to Pocket" option is selected in highlights
        navigate('about:preferences#home')
        click(AboutPreferences.FIND_IN_OPTIONS)
        paste('Highlights')
        click(most_recent_download_checkbox)
        click(pages_saved_to_pocket_checkbox)
        new_tab()
        highlights_page_saved_to_pocket_exists = exists(highlights_page_saved_to_pocket,
                                                        FirefoxSettings.FIREFOX_TIMEOUT)
        assert highlights_page_saved_to_pocket_exists, 'Page saved in pockets is not displayed in Highlights'
