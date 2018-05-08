# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is an experiment for OCR in region'
        # self.exclude = Platform.ALL

    @staticmethod
    def generate_region_by_markers(top_left_marker_img=None, bottom_right_marker_img=None):
        try:
            wait(top_left_marker_img, 10)
            exists(bottom_right_marker_img, 10)
        except Exception as err:
            logger.error('Unable to find page markers')
            raise err

        top_left_pos = find(top_left_marker_img)
        hover(top_left_pos, 1)
        bottom_right_pos = find(bottom_right_marker_img)
        hover(bottom_right_pos, 1)

        marker_width, marker_height = get_asset_img_size(bottom_right_marker_img)

        return Region(top_left_pos.x,
                      top_left_pos.y,
                      (bottom_right_pos.x + marker_width),
                      bottom_right_pos.y - top_left_pos.y + marker_height)

    def run(self):

        url = 'file:///' + get_module_dir() + '/iris/tests/unit_tests/assets/ocr-page.html'
        navigate(url)

        top_left_marker = 'ut-top-left.png'
        bottom_right_marker = 'ut-bottom-right.png'

        page_region = self.generate_region_by_markers(top_left_marker, bottom_right_marker)

        page_region.debug()

        # page_region.find('ut-top-left.png')
        # page_region.find('ut-bottom-right.png')

        # print(page_region.text())

        # assert_true(self, page_region.exists('Lorem'), 'Word: Lorem should exist')

        # search_for_text = 'Contents'
        # time.sleep(4)
        #
        # new_region = Region(0, 0, 200, screen_height)
        #
        # all_text = new_region.text()
        # logger.info(all_text)
        #
        # if search_for_text in all_text:
        #     print ('Text Found')
        #
        # new_region.hover(search_for_text)
        # hover(Location(0, 0))
        #
        # find_location = new_region.find(search_for_text)
        # hover(find_location)
        # hover(Location(0, 0))
        #
        # new_region.click(search_for_text)
        # hover(Location(0, 0))
        #
        # time.sleep(2)
