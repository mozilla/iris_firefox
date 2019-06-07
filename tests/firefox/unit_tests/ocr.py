# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='This is a unit test for ocr.'
    )
    def run(self, firefox):
        navigate(PathManager.get_current_test_asset_dir('ocr.html'))

        top_left_marker = Pattern('ut-top-left.png')
        bottom_right_marker = Pattern('ut-bottom-right.png')

        page_region = RegionUtils.generate_region_by_markers(top_left_marker, bottom_right_marker)
        left_half_page_region = Region(page_region.x, page_region.y, page_region.width / 3 + 100, page_region.height)

        assert left_half_page_region.exists('Lorem'), 'Word found'
        assert left_half_page_region.exists('Library'), 'Word found'
        assert left_half_page_region.exists('Find in This Page'), 'Phrase found'
        assert left_half_page_region.exists('New Private Window'), 'Phrase found'

        hover(left_half_page_region.find('Library'))
        hover(left_half_page_region.find('Find in This Page'))
        hover(left_half_page_region.find('New Private Window'))

        assert left_half_page_region.exists('The quick brown'), 'Phrase found'
        assert left_half_page_region.exists('fox jumps over the lazy dog.'), 'Phrase found'
        assert left_half_page_region.exists('jumps over the'), 'Phrase found'
        assert left_half_page_region.exists('The quick brown fox jumps over the lazy dog.'), 'Phrase found'

        hover(left_half_page_region.find('The quick brown'))
        hover(left_half_page_region.find('fox jumps over the lazy dog.'))
        hover(left_half_page_region.find('jumps over the'))
        hover(left_half_page_region.find('The quick brown fox jumps over the lazy dog.'))

        click(top_left_marker)
        time.sleep(Settings.DEFAULT_UI_DELAY_SHORT)

        assert left_half_page_region.exists('Library'), 'Word found'
        assert left_half_page_region.exists('Find in This Page'), 'Phrase found'
        assert left_half_page_region.exists('New Private Window'), 'Phrase found'

        click(bottom_right_marker)
        time.sleep(Settings.DEFAULT_UI_DELAY_SHORT)

        assert left_half_page_region.exists('Quisque'), '"Quisque" found'
        assert left_half_page_region.exists('Library'), 'Word found'
        assert left_half_page_region.exists('Find in This Page'), 'Phrase found'
        assert left_half_page_region.exists('New Private Window'), 'Phrase found'

        click(NavBar.HAMBURGER_MENU)
        time.sleep(Settings.DEFAULT_UI_DELAY_SHORT)

        hamburger_menu_region = create_region_from_image(NavBar.HAMBURGER_MENU)

        assert hamburger_menu_region.exists('Sign in to Sync'), '"Sign in to Sync" found'
        assert hamburger_menu_region.exists('Content Blocking'), '"Content Blocking" found'
