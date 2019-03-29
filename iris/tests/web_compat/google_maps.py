# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Web compatibility test for maps.google.com'
        self.enabled = False

    def run(self):
        url = 'maps.google.com/'
        google_maps_search_bar_magnifier_pattern = Pattern('google_maps_search_bar_magnifier.png')
        google_maps_item_searched_pattern = Pattern('google_maps_item_searched.png')

        navigate(url)

        expected_1 = exists(google_maps_search_bar_magnifier_pattern, 20)
        assert_true(self, expected_1, 'The page is successfully loaded.')

        # Type 'Mediterranean Sea' in the search bar.
        click(google_maps_search_bar_magnifier_pattern.target_offset(-100, 15))
        time.sleep(2)
        paste('Mediterranean Sea')
        type(Key.ENTER)

        expected_2 = exists(google_maps_item_searched_pattern, 20)
        assert_true(self, expected_2, 'Item searched found.')
