# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is an experiment for OCR in region'
        # self.exclude = Platform.ALL

    def run(self):
        url = 'file:///' + get_module_dir() + '/iris/tests/unit_tests/assets/ocr.html'
        navigate(url)

        top_left_marker = 'ut-top-left.png'
        bottom_right_marker = 'ut-bottom-right.png'

        page_region = generate_region_by_markers(top_left_marker, bottom_right_marker)
        page_region.debug()
        logger.info(page_region.text())

        assert_true(self, page_region.exists('Lorem'), 'Word: Lorem should exist')
