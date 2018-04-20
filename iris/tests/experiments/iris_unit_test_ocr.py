# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is an experiment for OCR in region'

    def run(self):
        url = 'https://en.wikipedia.org/wiki/Main_Page'
        navigate(url)

        search_for_text = 'Contents'
        time.sleep(4)

        new_region = Region(0, 0, 200, screen_height)

        all_text = new_region.text()
        logger.info(all_text)

        if search_for_text in all_text:
            print ('Text Found')

        new_region.hover(search_for_text)
        hover(Location(0, 0))

        find_location = new_region.find(search_for_text)
        hover(find_location)
        hover(Location(0, 0))

        new_region.click(search_for_text)
        hover(Location(0, 0))

        time.sleep(2)
