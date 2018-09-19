# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *
from iris.api.core.util.update_rules import *


class Test(BaseTest):

    def __init__(self, app):
        BaseTest.__init__(self, app)
        self.meta = 'This is a test for Firefox manual update.'

    def setup(self):
        BaseTest.setup(self)
        self.set_profile_pref('app.update.log;true')
        self.maximize_window = False

    def run(self):
        update_restart_pattern = Pattern('manual_restart_to_update_button.png')
        firefox_up_to_date_pattern = Pattern('firefox_up_to_date.png')
        current_version = self.app.args.firefox
        channel = self.app.fx_channel
        rule_dict = get_rule_for_current_channel(channel)
        if rule_dict is None:
            raise ValueError('No rules found for %s channel. Please update config.ini file.' % channel)

        starting_condition = rule_dict['starting_condition']
        watershed_version = rule_dict['watershed_version']
        latest_version = rule_dict['latest_version']
        assert_contains(self, current_version, get_firefox_version(self.app.fx_path),
                        'Firefox version is correct (%s).' % current_version)

        while current_version != latest_version:
            starting_version = current_version
            watershed_required = is_watershed_version_required(current_version, starting_condition)
            if watershed_required:
                logger.info('Current version: %s, watershed required: %s.' % (current_version, watershed_version))
                current_version = watershed_version
            else:
                logger.info('Current version: %s, watershed not required. Updating to latest: %s.'
                            % (current_version, latest_version))
                current_version = latest_version

            confirm_firefox_launch(self.app)
            open_about_firefox()
            wait(update_restart_pattern, 200)
            type(Key.ESC)
            restart_firefox(self.app.fx_path, self.profile_path, url=self.app.base_local_web_url)
            assert_contains(self, current_version, get_firefox_version(self.app.fx_path),
                            'Firefox successfully updated from %s to %s.' % (starting_version, current_version))

        if current_version == latest_version:
            open_about_firefox()
            wait(firefox_up_to_date_pattern, 20)
            type(Key.ESC)
            assert_contains(self, current_version, get_firefox_version(self.app.fx_path),
                            'Firefox version is correct (%s).' % current_version)

        new_tab()
        navigate(LocalWeb.MOZILLA_TEST_SITE)
        expected = exists(LocalWeb.MOZILLA_LOGO, 5)
        assert_true(self, expected, 'Manual update sanity test passed.')
