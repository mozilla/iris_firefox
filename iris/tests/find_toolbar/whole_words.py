# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = '"Whole Words" button works properly'
        self.test_case_id = '127453'
        self.test_suite_id = '2085'
        self.locales = ['en-US']

    def run(self):

        find_in_page_icon_pattern = Pattern('find_in_page_icon.png')
        tester_label_pattern = Pattern('tester_label.png')
        whole_words_button_pattern = Pattern('whole_words_button.png')
        test_selected_label_pattern = Pattern('test_selected_label.png')
        other_label_is_not_highlighted = Pattern('testex_label.png')
        second_selected_label_pattern = Pattern('text_label_selected_second.png')

        test_page_local = self.get_asset_path('words.html')
        navigate(test_page_local)

        soap_label_exists = exists(tester_label_pattern, 20)

        assert_true(self, soap_label_exists, 'The page is successfully loaded.')

        open_find()
        edit_select_all()
        edit_delete()

        find_toolbar_opened = exists(find_in_page_icon_pattern, 10)

        assert_true(self, find_toolbar_opened, 'Find Toolbar is opened.')

        type('test', interval=1)
        click(whole_words_button_pattern)

        selected_label_exists = exists(test_selected_label_pattern, 5)

        assert_true(self, selected_label_exists,
                    'All the matching words/characters are found. The first one has a green background highlighted, '
                    'and the others are not highlighted.')

        type(Key.F3, interval=1)

        first_label_is_green = exists(second_selected_label_pattern, 5)
        other_label_is_not_highlighted = exists(other_label_is_not_highlighted, 5)

        assert_true(self, first_label_is_green, 'The next matching words/characters have a green background highlighted')
        assert_true(self, other_label_is_not_highlighted, 'The other is not highlighted')
