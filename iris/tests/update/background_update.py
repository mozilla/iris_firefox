# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This is a test for Firefox background update.'
        self.exclude = Platform.ALL

    def setup(self):
        BaseTest.setup(self)
        self.set_profile_pref({'app.update.auto': True,
                               'app.update.interval': 7200,
                               'app.update.badgeWaitTime': 10,
                               'app.update.lastUpdateTime.background-update-timer': 1,
                               'app.update.promptWaitTime': 30,
                               'app.update.timerMinimumDelay': 10,
                               'app.update.channel': '%s-cdntest' % self.browser.channel})
        self.maximize_window = False

    def run(self):
        update_restart_pattern = Pattern('background_update_menu_notification.png')
        firefox_up_to_date_pattern = Pattern('firefox_up_to_date.png')

        version = parse_args().firefox
        current_version = version if '-dev' not in version else version.replace('-dev', '')
        channel = self.browser.channel
        rules_dict = get_rule_for_current_channel(channel, current_version)

        if rules_dict is None:
            raise ValueError('No rules found for %s channel. Please update config.ini file.' % channel)

        starting_condition = rules_dict['starting_condition']
        update_steps_list = rules_dict['steps'].split(',')

        assert_contains(self, current_version, get_firefox_version(self.browser.path),
                        'Firefox version is correct (%s)' % current_version)

        if is_update_required(current_version, starting_condition):
            for update_step in update_steps_list:

                if update_step == 'latest':
                    update_step = self.browser.latest_version

                logger.info('Current version: %s, updating to version: %s.' % (current_version, update_step))

                try:
                    reset_mouse()
                    wait(update_restart_pattern, 120)
                except FindError:
                    raise FindError('Background update hamburger menu icon notification did not appear, aborting.')

                restart_firefox(self,
                                self.browser.path,
                                self.profile_path,
                                self.base_local_web_url)

                assert_contains(self,
                                update_step,
                                get_firefox_version(self.browser.path),
                                'Firefox successfully updated from %s to %s.' % (current_version, update_step))

                current_version = update_step

        open_about_firefox()
        wait(firefox_up_to_date_pattern, 20)
        type(Key.ESC)
        assert_contains(self, current_version, get_firefox_version(self.browser.path),
                        'Firefox version is correct (%s)' % current_version)

        new_tab()
        navigate(LocalWeb.MOZILLA_TEST_SITE)
        expected = exists(LocalWeb.MOZILLA_LOGO, 10)
        assert_true(self, expected, 'Background update sanity test passed.')
