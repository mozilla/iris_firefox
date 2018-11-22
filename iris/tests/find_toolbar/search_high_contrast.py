# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Search when High Contrast is activated'
        self.test_case_id = '127254'
        self.test_suite_id = '2085'
        self.locales = ['en-US']

    def run(self):
        '''
        "1. Windows: Go to Personalise> Themes> Theme Settings and activate a High Contrast Theme.
         Ubuntu: Install ""gnome-control-center""- System settings-Appearance

         Expected Result:

         - The theme is activated.

         2. Open Firefox and navigate to a popular website (Google.com, Amazon.com, NYTimes etc).

         Expected Result:

         - The page is successfully loaded.

         3. Open the Find Toolbar.

         Expected Result:

         - Find Toolbar is opened.

         4. Search for a term that appears more than once in the page.

         Expected Result:

         - All the matching words/characters are found. The first one has a green background highlighted, and the others are not highlighted.

         5. Zoom the page in/out and check the highlighted items.

         Expected Result:

         - The highlight of the found items doesn't affect the visibility of other words/letters. No misplacement of the highlight is visible."
        '''

        find_in_page_bar_contrast_pattern = Pattern('find_in_page_bar_contrast.png')

        soap_page_url_contrast_pattern = Pattern('soap_page_url_contrast.png')
        see_label_contrast_pattern = Pattern('see_label_contrast.png')
        see_label_unhighlited_contrast_pattern = Pattern('see_label_unhighlited_contrast.png')
        see_label_zoom_in_contrast_pattern = Pattern('see_label_zoom_in_contrast.png')
        see_label_zoom_out_contrast_pattern = Pattern('see_label_zoom_out_contrast.png')

        # windows theme settings
        win_type_here_to_search_pattern = Pattern('win_type_here_to_search.png')
        win_high_contrast_settings_pattern = Pattern('win_high_contrast_settings.png')
        win_off_high_contrast_button_theme_pattern = Pattern('win_off_high_contrast_theme.png')
        win_on_high_contrast_theme_pattern = Pattern('high_contrast_is_on.png') # high contrast is on
        win_close_active_window_pattern = Pattern('win_close_active_window.png')

        if Settings.is_windows():
            if get_os_version() == 'win7':
                pass
            else:
                win_type_here_to_search_exists = exists(win_type_here_to_search_pattern, 10)
                type_here_theme_options_location = find(win_type_here_to_search_pattern)
                click(Location(type_here_theme_options_location.x+5,
                               type_here_theme_options_location.y+5), 1)

                paste('themes and related settings')
                type(Key.ENTER)

                win_high_contrast_settings_exists = exists(win_high_contrast_settings_pattern, 10)
                win_high_contrast_settings_location = find(win_high_contrast_settings_pattern)
                click(Location(win_high_contrast_settings_location.x+10,
                               win_high_contrast_settings_location.y+10), 1)

                win_off_high_contrast_theme_exists = exists(win_off_high_contrast_button_theme_pattern, 10)
                win_off_high_contrast_theme_location = find(win_off_high_contrast_button_theme_pattern)
                click(Location(win_off_high_contrast_theme_location.x+7,
                               win_off_high_contrast_theme_location.y+7), 1)

                # delay for high contrast to be enabled
                time.sleep(5)
                high_contrast_enabled = exists(win_on_high_contrast_theme_pattern, 5)
                assert_true(self, high_contrast_enabled, 'High contrast option enabled on Windows 10')

                win_close_active_window_location = find(win_close_active_window_pattern)
                click(win_close_active_window_pattern, 1)

        test_page_local = self.get_asset_path('wiki_soap.html')
        navigate(test_page_local)

        soap_page_loaded_exists = exists(soap_page_url_contrast_pattern, 20)

        assert_true(self, soap_page_loaded_exists, 'The page is successfully loaded.')

        # delay for win 10 to prevent select all content
        time.sleep(Settings.SYSTEM_DELAY)

        open_find()
        edit_select_all()
        edit_delete()

        find_toolbar_opened = exists(find_in_page_bar_contrast_pattern, 10)

        assert_true(self, find_toolbar_opened, 'Find Toolbar is opened.')

        type('see', interval=1)
        type(Key.ENTER)

        selected_label_exists = exists(see_label_contrast_pattern, 5)
        unhighlighted_label_exists = exists(see_label_unhighlited_contrast_pattern, 5)

        assert_true(self, selected_label_exists, 'The first one has a green background highlighted.')
        assert_true(self, unhighlighted_label_exists,
                    'The others are not highlighted.')

        zoom_in()

        selected_label_exists = exists(see_label_zoom_in_contrast_pattern, 5)

        assert_true(self, selected_label_exists,
                    'Zoom in: The highlight of the found items does not affect the visibility of other words/letters')

        zoom_out()
        zoom_out()

        selected_label_exists = exists(see_label_zoom_out_contrast_pattern, 5)

        assert_true(self, selected_label_exists,
                    'Zoom out: The highlight of the found items does not affect the visibility of other words/letters')

        # quit of high contrast mode

        click(Location(type_here_theme_options_location.x + 5,
                       type_here_theme_options_location.y + 5), 1)

        paste('themes and related settings')
        type(Key.ENTER)

        click(Location(win_high_contrast_settings_location.x + 10,
                       win_high_contrast_settings_location.y + 10), 1)

        click(Location(win_off_high_contrast_theme_location.x + 7,
                       win_off_high_contrast_theme_location.y + 7), 1)

        contrast_mode_off = exists(win_off_high_contrast_button_theme_pattern, 10)

        # close theme settings window
        click(Location(win_close_active_window_location.x+2, win_close_active_window_location.y+2), 1)

        assert_true(self, contrast_mode_off,
                    'Exited contrast mode')
