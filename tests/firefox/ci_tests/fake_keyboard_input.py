# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.
from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description='Created to test fake keyboard inputs',
        locale=['en-US'],
        platform=OSPlatform.LINUX
    )
    def run(self, firefox):
        history_empty_pattern = Pattern('history_empty.png')

        new_tab()
        navigate(LocalWeb.MOZILLA_TEST_SITE)
        expected_1 = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert expected_1, 'Mozilla page loaded successfully.'

        new_tab()
        navigate(LocalWeb.FIREFOX_TEST_SITE)
        expected_2 = exists(LocalWeb.FIREFOX_LOGO, 10)
        assert expected_2, 'Firefox page loaded successfully.'

        history_sidebar()

        for step in open_clear_recent_history_window():
            assert step.resolution, step.message

        for i in range(4):
            type(Key.DOWN)

        logger.debug('TAB')
        type(Key.TAB)
        logger.debug('TAB')
        type(Key.TAB)
        for i in range(5):
            type(Key.DOWN)
        logger.debug('SPACE')
        type(Key.SPACE)
        type(Key.DOWN)
        type(Key.SPACE)
        logger.debug('ENTER')
        type(Key.ENTER)

        restore_firefox_focus()

        expected_4 = exists(history_empty_pattern.similar(0.9), 10)
        assert expected_4, 'All the history was cleared successfully.'
