# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Navigate through found items'
        self.test_case_id = '127249'
        self.test_suite_id = '2085'
        self.locales = ['en-US']

    def run(self):
        soap_label_pattern = Pattern('soap_label.png')
        see_label_pattern = Pattern('see_label.png')
        see_label_not_highlighted_pattern = Pattern('see_label_unhighlited.png')
        find_in_page_icon_pattern = Pattern('find_in_page_icon.png')
        arrow_up_button_pattern = Pattern('arrow_up_button.png')
        arrow_down_button_pattern = Pattern('arrow_down_button.png')
        cleaning_see_label_pattern = Pattern('cleaning_see_label.png')
        one_of_five_label_pattern = Pattern('1_of_5_matches_label.png')
        two_of_five_label_pattern = Pattern('2_of_5_matches_label.png')

        wiki_page_local = self.get_asset_path('soap.html')
        navigate(wiki_page_local)
        soap_label_exists = exists(soap_label_pattern, 20)
        assert_true(self, soap_label_exists, 'The page is successfully loaded.')

        # open and clear find toolbar
        open_find()
        edit_select_all()
        edit_delete()

        find_toolbar_opened = exists(find_in_page_icon_pattern, 10)

        assert_true(self, find_toolbar_opened, 'Find Toolbar is opened.')

        type('see', interval=1)
        type(Key.ENTER)

        selected_label_exists = exists(see_label_pattern, 1)
        not_highlighted_label_exists = exists(see_label_not_highlighted_pattern, 1)

        assert_true(self, selected_label_exists, 'The first one has a green background highlighted.')
        assert_true(self, not_highlighted_label_exists,
                    'The others are not highlighted.')

        click(arrow_up_button_pattern)
        cleaning_see_label_exists = exists(cleaning_see_label_pattern, 1)

        assert_true(self, cleaning_see_label_exists, 'Navigation up works fine.')

        click(arrow_down_button_pattern)
        selected_label_exists = exists(see_label_pattern, 1)

        assert_true(self, selected_label_exists, 'Navigation down works fine.')

        click(arrow_up_button_pattern)
        one_of_five_label_exists = exists(one_of_five_label_pattern, 1)

        assert_true(self, one_of_five_label_exists, 'The number of the highlighted item changes when navigating')

        click(arrow_down_button_pattern)
        two_of_five_label_exists = exists(two_of_five_label_pattern, 1)

        assert_true(self, two_of_five_label_exists, 'The number of the highlighted item changes when navigating.')
