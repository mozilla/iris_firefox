# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


def confirm_hover(hover_region, hovered_element):
    assert hover_region.exists(hovered_element), 'Hover confirmed'


class Test(FirefoxTest):

    @pytest.mark.details(
        description='This is a unit test for hover, and click.'
    )
    def run(self, firefox):
        t_left = Pattern('ut-top-left.png')
        b_right = Pattern('ut-bottom-right.png')

        hover_t_left = Pattern('ut-hover-top.png')
        hover_b_right = Pattern('ut-hover-bottom.png')
        click_t_left = Pattern('ut-click-top.png')
        click_b_right = Pattern('ut-click-bottom.png')

        navigate(PathManager.get_current_test_asset_dir('mouse-events.html'))
        wait(t_left, 10)

        desktop_i = Pattern('ut-desktop.png')
        keyboard_i = Pattern('ut-keyboard.png')
        power_i = Pattern('ut-power-off.png')
        upload_i = Pattern('ut-upload.png')
        save_i = Pattern('ut-save.png')

        desktop_pattern = Pattern('ut-desktop.png')
        keyboard_pattern = Pattern('ut-keyboard.png')
        power_pattern = Pattern('ut-power-off.png')
        upload_pattern = Pattern('ut-upload.png')
        save_pattern = Pattern('ut-save.png')

        last_hover_region = RegionUtils.generate_region_by_markers(hover_t_left, hover_b_right)
        last_click_region = RegionUtils.generate_region_by_markers(click_t_left, click_b_right)

        # ---- HOVER TESTS ----

        # General hover
        logger.debug('Test hover on page by image names')
        hover(desktop_i)
        confirm_hover(last_hover_region, desktop_i)
        hover(keyboard_i)
        confirm_hover(last_hover_region, keyboard_i)
        hover(power_i)
        confirm_hover(last_hover_region, power_i)
        hover(upload_i)
        confirm_hover(last_hover_region, upload_i)
        hover(save_i)
        confirm_hover(last_hover_region, save_i)

        # Pattern hover
        logger.debug('Test hover on page with Pattern inputs')
        hover(desktop_pattern)
        confirm_hover(last_hover_region, desktop_pattern)
        hover(keyboard_pattern)
        confirm_hover(last_hover_region, keyboard_pattern)
        hover(power_pattern)
        confirm_hover(last_hover_region, power_pattern)
        hover(upload_pattern)
        confirm_hover(last_hover_region, upload_pattern)
        hover(save_pattern)
        confirm_hover(last_hover_region, save_pattern)

        # in Region general hover
        in_region = RegionUtils.generate_region_by_markers(t_left, b_right)

        logger.debug('Test hover in Region of page  by image names')
        in_region.hover(desktop_i)
        confirm_hover(last_hover_region, desktop_i)
        in_region.hover(keyboard_i)
        confirm_hover(last_hover_region, keyboard_i)
        in_region.hover(power_i)
        confirm_hover(last_hover_region, power_i)
        in_region.hover(upload_i)
        confirm_hover(last_hover_region, upload_i)
        in_region.hover(save_i)
        confirm_hover(last_hover_region, save_i)

        # in Region Pattern hover
        logger.debug('Test hover in Region with Pattern inputs')
        in_region.hover(desktop_pattern)
        confirm_hover(last_hover_region, desktop_pattern)
        in_region.hover(keyboard_pattern)
        confirm_hover(last_hover_region, keyboard_pattern)
        in_region.hover(power_pattern)
        confirm_hover(last_hover_region, power_pattern)
        in_region.hover(upload_pattern)
        confirm_hover(last_hover_region, upload_pattern)
        in_region.hover(save_pattern)
        confirm_hover(last_hover_region, save_pattern)

        # ---- CLICK TESTS ----

        # General click
        logger.debug('Test click on page by image names')
        click(desktop_i)
        confirm_hover(last_click_region, desktop_i)
        click(keyboard_i)
        confirm_hover(last_click_region, keyboard_i)
        click(power_i)
        confirm_hover(last_click_region, power_i)
        click(upload_i)
        confirm_hover(last_click_region, upload_i)
        click(save_i)
        confirm_hover(last_click_region, save_i)

        # Pattern click
        logger.debug('Test click on page with Pattern inputs')
        click(desktop_pattern)
        confirm_hover(last_click_region, desktop_pattern)
        click(keyboard_pattern)
        confirm_hover(last_click_region, keyboard_pattern)
        click(power_pattern)
        confirm_hover(last_click_region, power_pattern)
        click(upload_pattern)
        confirm_hover(last_click_region, upload_pattern)
        click(save_pattern)
        confirm_hover(last_click_region, save_pattern)

        logger.debug('Test click in Region of page  by image names')
        in_region.click(desktop_i)
        confirm_hover(last_click_region, desktop_i)
        in_region.click(keyboard_i)
        confirm_hover(last_click_region, keyboard_i)
        in_region.click(power_i)
        confirm_hover(last_click_region, power_i)
        in_region.click(upload_i)
        confirm_hover(last_click_region, upload_i)
        in_region.click(save_i)
        confirm_hover(last_click_region, save_i)

        # in Region Pattern click
        logger.debug('Test click in Region with Pattern inputs')
        in_region.click(desktop_pattern)
        confirm_hover(last_click_region, desktop_pattern)
        in_region.click(keyboard_pattern)
        confirm_hover(last_click_region, keyboard_pattern)
        in_region.click(power_pattern)
        confirm_hover(last_click_region, power_pattern)
        in_region.click(upload_pattern)
        confirm_hover(last_click_region, upload_pattern)
        in_region.click(save_pattern)
        confirm_hover(last_click_region, save_pattern)
