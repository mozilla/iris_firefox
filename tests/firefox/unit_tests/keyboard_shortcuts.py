# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='This is a unit test for keyboard events.',
        blocked_by={'id': 'issue_1862', 'platform': OSPlatform.WINDOWS}
    )
    def run(self, firefox):
        url = PathManager.get_current_test_asset_dir('keyboard-events.html')

        t_left = Pattern('ut-top-left.png')
        b_right = Pattern('ut-bottom-right.png')

        ut_alt = Pattern('ut-alt.png').similar(0.75)
        ut_ctrl = Pattern('ut-cmd-ctrl.png').similar(0.75)
        ut_reset_all = Pattern('ut-reset-all.png')
        ut_shift = Pattern('ut-shift.png').similar(0.75)

        navigate(url)
        wait(t_left, 10)

        page_region = RegionUtils.generate_region_by_markers(t_left, b_right)

        type('y', KeyModifier.CTRL)
        assert page_region.exists(ut_ctrl), 'Ctrl key trigger confirmed'
        click(ut_reset_all)

        type('y', KeyModifier.ALT)
        assert page_region.exists(ut_alt), 'Alt key trigger confirmed'
        click(ut_reset_all)

        type('y', KeyModifier.SHIFT)
        assert page_region.exists(ut_shift), 'Shift key trigger confirmed'
        click(ut_reset_all)
