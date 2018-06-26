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
        ut_reset_all = 'ut-reset-all.png'

        if position:
            click(position)
        else:
            click(ut_reset_all)

    def run(self):
        url = self.get_asset_path('keyboard-events.html')

        t_left = 'ut-top-left.png'
        b_right = 'ut-bottom-right.png'

        ut_all_modifiers = 'ut-all-modifiers.png'
        ut_alt = 'ut-alt.png'
        ut_alt_shift = 'ut-alt-shift.png'
        ut_ctrl = 'ut-cmd-ctrl.png'
        ut_ctrl_alt = 'ut-cmd-ctrl-alt.png'
        ut_ctrl_shift = 'ut-cmd-ctrl-shift.png'
        ut_reset_all = 'ut-reset-all.png'
        ut_shift = 'ut-shift.png'

        navigate(url)
        wait(t_left)

        page_region = generate_region_by_markers(t_left, b_right)

        temp_pos = page_region.find(ut_reset_all)
        width, height = get_asset_img_size(ut_reset_all)
        reset_btn = Location(temp_pos.getX() + width / 2, temp_pos.getY() + height / 2)

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
