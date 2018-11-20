# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Search on a window with a different size'
        self.test_case_id = '127247'
        self.test_suite_id = '2085'
        self.locales = ['en-US']

    def run(self):

        find_in_page_icon_pattern = Pattern('find_in_page_icon.png')
        soap_label_pattern = Pattern('soap_label.png')
        match_case_button_pattern = Pattern('match_case_button.png')
        soap_xml_label_pattern = Pattern('soap_xml_label.png')
        soap_envelope_label_selected_pattern = Pattern('soap_envelope_label_selected.png')

        test_page_local = self.get_asset_path('wiki_soap.html')
        navigate(test_page_local)

        soap_label_exists = exists(soap_label_pattern, 20)

        assert_true(self, soap_label_exists, 'The page is successfully loaded.')

        if Settings.is_mac():
            key_down(Key.CMD)
            key_down(Key.CTRL)
            type('f')
            key_up(Key.CMD)
            key_up(Key.CTRL)
            key_up(Key.CTRL)
            key_up(Key.CMD)
        else:
            type(Key.F11)

        open_find()
        edit_select_all()
        edit_delete()

        find_toolbar_opened = exists(find_in_page_icon_pattern, 10)

        assert_true(self, find_toolbar_opened, 'Find Toolbar is opened.')

        type('soap', interval=1)
        click(match_case_button_pattern)

        find_next()

        selected_label_exists = exists(soap_envelope_label_selected_pattern, 5)
        unselected_label_exists = exists(soap_xml_label_pattern, 5)

        assert_true(self, selected_label_exists, 'The first one has a green background highlighted.')
        assert_true(self, unselected_label_exists, 'The others are not highlighted.')

        if Settings.is_mac():
            key_down(Key.CMD)
            key_down(Key.CTRL)
            type('f')
            key_up(Key.CMD)
            key_up(Key.CTRL)
        else:
            type(Key.F11)

        selected_label_exists = exists(soap_envelope_label_selected_pattern, 5)
        unselected_label_exists = exists(soap_xml_label_pattern, 5)

        assert_true(self, selected_label_exists, 'The first one has a green background highlighted.')
        assert_true(self, unselected_label_exists,
                    'The others are not highlighted.')

