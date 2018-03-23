# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from test_case import *


class test(base_test):

    def __init__(self, app):
        base_test.__init__(self, app)
        self.meta = "This is a test of new tab preferences search"

    def run(self):

        url = "about:home"
        customize_new_tab_page_image = "customize_new_tab_icon.png"
        tab_preference_search_button = "tab_preference_search_button.png"
        tab_search_section = "search_the_web.png"

        navigate(url)

        if exists(customize_new_tab_page_image, 10):
            try:
                click(customize_new_tab_page_image)
                if exists(tab_preference_search_button, 2):
                    try:
                        click(tab_preference_search_button)
                        if waitVanish(tab_search_section, 2):
                            result = "PASS"
                        else:
                            result = "FAIL"
                    except:
                        result = "FAIL"
                else:
                    result = "FAIL"
            except:
                result = "FAIL"
        else:
            result = "FAIL"

        print result
