
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Bug 1419819 - The View/Hide Previous Tabs toggle button overlaps the adjacent label'
        self.test_case_id = '178003'
        self.test_suite_id = '68'
        self.locales = ['en-US']

    def run(self):
        restore_session_button_pattern = Pattern('restore_session_button.png')
        view_previous_tabs_pattern = Pattern('view_previous_tabs_label.png')
        hide_previous_tabs_pattern = Pattern('hide_previous_tabs_label.png')
        view_form_is_opened_pattern = Pattern('view_form_is_opened.png')

        navigate('about:sessionrestore')

        about_session_restore_exists = exists(restore_session_button_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, about_session_restore_exists, 'The *about:sessionrestore* is successfully displayed')

        view_previous_tabs_exists = exists(view_previous_tabs_pattern, Settings.FIREFOX_TIMEOUT)
        assert_true(self, view_previous_tabs_exists, '*View Previous Tabs* and label nearby is displayed correctly')

        click(view_previous_tabs_pattern)

        try:
            view_previous_tabs_not_exists = wait_vanish(view_previous_tabs_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
            assert_true(self, view_previous_tabs_not_exists, '*View Previous Tabs* and label nearby is disappeared')
        except FindError:
            raise FindError('*View Previous Tabs* and label nearby still exists')

        hide_previous_tabs_exists = exists(hide_previous_tabs_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, hide_previous_tabs_exists, '*Hide Previous Tabs* and label nearby is displayed correctly')

        view_form_is_opened_exists = exists(view_form_is_opened_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
        assert_true(self, view_form_is_opened_exists, 'View form is displayed and view button properly works')

        click(hide_previous_tabs_pattern)

        try:
            hide_previous_tabs_not_exists = wait_vanish(hide_previous_tabs_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
            assert_true(self, hide_previous_tabs_not_exists, '*Hide Previous Tabs* and label nearby is disappeared')
        except FindError:
            raise FindError('*Hide Previous Tabs* and label nearby still exists')

        try:
            view_form_is_opened_not_exists = wait_vanish(view_form_is_opened_pattern, Settings.SHORT_FIREFOX_TIMEOUT)
            assert_true(self, view_form_is_opened_not_exists, 'View form is disappeared and hide button properly works')
        except FindError:
            raise FindError('View form still exists')
