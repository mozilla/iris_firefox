# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a unit test for keyboard events.'

    @staticmethod
    def reset_all_modifiers(position):
        logger.debug('Reset all modifiers')
        ut_reset_all = Pattern('ut-reset-all.png')

        if position:
            click(position)
        else:
            click(ut_reset_all)

    def run(self):
        url = self.get_asset_path('keyboard-events.html')

        t_left = Pattern('ut-top-left.png')
        b_right = Pattern('ut-bottom-right.png')

        ut_alt = Pattern('ut-alt.png')
        ut_ctrl = Pattern('ut-cmd-ctrl.png')
        ut_reset_all = Pattern('ut-reset-all.png')
        ut_shift = Pattern('ut-shift.png')

        navigate(url)
        wait(t_left, 10)

        page_region = generate_region_by_markers(t_left, b_right)

        temp_pos = page_region.find(ut_reset_all)
        width, height = get_image_size(ut_reset_all)
        reset_btn = Location(temp_pos.x + width / 2, temp_pos.y + height / 2)

        # Test modifiers
        type('y', KeyModifier.CTRL)
        assert_true(self, page_region.exists(ut_ctrl, 0.99), 'Ctrl key trigger confirmed')
        self.reset_all_modifiers(reset_btn)

        type('y', KeyModifier.ALT)
        assert_true(self, page_region.exists(ut_alt, 0.99), 'Alt key trigger confirmed')
        self.reset_all_modifiers(reset_btn)

        type('y', KeyModifier.SHIFT)
        assert_true(self, page_region.exists(ut_shift, 0.99), 'Shift key trigger confirmed')
        self.reset_all_modifiers(reset_btn)
