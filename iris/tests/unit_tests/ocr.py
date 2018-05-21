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
        half_page_region = Region(page_region.x, page_region.y, page_region.w / 3, page_region.h)
        half_page_region.debug()

        assert_true(self, half_page_region.exists('Library'), 'Word found')
        assert_true(self, half_page_region.exists('Find in This Page'), 'Phrase found')
        assert_true(self, half_page_region.exists('New Private Window'), 'Phrase found')

        hover(half_page_region.find('Library'))
        hover(half_page_region.find('Find in This Page'))
        hover(half_page_region.find('New Private Window'))

        assert_true(self, half_page_region.exists('The quick brown'), 'Phrase found')
        assert_true(self, half_page_region.exists('fox jumps over the lazy dog.'), 'Phrase found')
        assert_true(self, half_page_region.exists('jumps over the'), 'Phrase found')
        assert_true(self, half_page_region.exists('The quick brown fox jumps over the lazy dog.'), 'Phrase found')

        hover(half_page_region.find('The quick brown'))
        hover(half_page_region.find('fox jumps over the lazy dog.'))
        hover(half_page_region.find('jumps over the'))
        hover(half_page_region.find('The quick brown fox jumps over the lazy dog.'))

        # Change background color to grey
        click(top_left_marker)
        time.sleep(2)
        half_page_region.debug()
        assert_true(self, half_page_region.exists('Library'), 'Word found')
        assert_true(self, half_page_region.exists('Find in This Page'), 'Phrase found')
        assert_true(self, half_page_region.exists('New Private Window'), 'Phrase found')

        click(bottom_right_marker)
        time.sleep(2)
        half_page_region.debug()
        assert_true(self, half_page_region.exists('Library'), 'Word found')
        assert_true(self, half_page_region.exists('Find in This Page'), 'Phrase found')
        assert_true(self, half_page_region.exists('New Private Window'), 'Phrase found')
