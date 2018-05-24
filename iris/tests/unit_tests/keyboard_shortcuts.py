# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a unit test for keyboard events.'
        self.reset_all_pos = None
        # self.exclude = Platform.ALL

    def reset_all_modifiers(self):
        logger.debug('Reset all modifiers')
        if self.reset_all_pos:
            click(self.reset_all_pos)
        else:
            click('ut-reset-all.png')

    def run(self):
        # @todo load this via assets
        url = 'file:///' + get_module_dir() + '/iris/tests/unit_tests/assets/keyboard-events.html'

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
        # time.sleep(2)

        self.reset_all_pos = page_region.find(ut_reset_all).offset(25, 10)

        # Test modifiers
        type('y', KeyModifier.CTRL)
        assert_true(self, page_region.exists(ut_ctrl, 0.99), 'Key trigger confirmed')
        self.reset_all_modifiers()

        type('y', KeyModifier.ALT)
        assert_true(self, page_region.exists(ut_alt, 0.99), 'Key trigger confirmed')
        self.reset_all_modifiers()

        type('y', KeyModifier.SHIFT)
        assert_true(self, page_region.exists(ut_shift, 0.99), 'Key trigger confirmed')
        self.reset_all_modifiers()
