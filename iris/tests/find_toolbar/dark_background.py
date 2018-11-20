# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Check the highlight of the found items on a page with dark background'
        self.test_case_id = '127242'
        self.test_suite_id = '2085'
        self.locales = ['en-US']

    def run(self):

        find_in_page_icon_pattern = Pattern('find_in_page_icon.png')
        work_in_label_pattern = Pattern('work_in_selected_label.png')
        instagram_unselected_pattern = Pattern('instagram_unselected_label.png')

        test_page_local = self.get_asset_path('dark_backgound.html')
        navigate(test_page_local)

        page_loaded = exists(instagram_unselected_pattern, 100)

        assert_true(self, page_loaded, 'The page is successfully loaded.')

        open_find()
        edit_select_all()
        edit_delete()

        find_toolbar_opened = exists(find_in_page_icon_pattern, 10)

        assert_true(self, find_toolbar_opened, 'Find Toolbar is opened.')

        type('in', interval=1)

        selected_label_exists = exists(work_in_label_pattern, 15)
        unselected_label_exists = exists(instagram_unselected_pattern, 5)

        assert_true(self, selected_label_exists, 'The first one has a green background highlighted.')
        assert_true(self, unselected_label_exists, 'The others are not highlighted.')

