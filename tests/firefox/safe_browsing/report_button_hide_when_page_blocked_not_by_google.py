# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):

    @pytest.mark.details(
        description=' The report button is hidden when the page is blocked not by google. '
                    '(we only report to google server)',
        test_case_id='50353',
        test_suite_id='69',
        locale=['en-US'],
    )
    def run(self, firefox):
        not_blocked_by_google_page_pattern = Pattern('deceptive_site_logo.png')
        see_details_button_pattern = Pattern('see_details_button.png')
        get_me_out_of_here_button_pattern = Pattern('get_me_out_of_here_button.png')
        this_isnt_a_deceptive_site_button_pattern = Pattern('this_isnt_a_deceptive_site_button.png')
        ignore_the_risk_link_pattern = Pattern('ignore_the_risk_link.png')

        navigate('http://www.itisatrap.org/firefox/its-a-trap.html')

        not_blocked_by_google_page_displayed = exists(not_blocked_by_google_page_pattern,
                                                      FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert not_blocked_by_google_page_displayed, 'The page that is not blocked by google opened'

        see_details_button_displayed = exists(see_details_button_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert see_details_button_displayed, 'The See details button displayed'

        click(see_details_button_pattern)

        ignore_the_risk_link_displayed = exists(ignore_the_risk_link_pattern, FirefoxSettings.SHORT_FIREFOX_TIMEOUT)
        assert ignore_the_risk_link_displayed, '"ignore the risk" link displayed'

        edit_select_all()

        edit_copy()

        text_displayed = get_clipboard().replace('\n', '').replace('\r', '')

        assert 'itisatrap.org has been reported as a deceptive site. You can report a detection problem or ignore ' \
               'the risk and go to this unsafe site.Learn more about deceptive sites and phishing at ' \
               'www.antiphishing.org. Learn more about Firefox’s Phishing and Malware Protection at ' \
               'support.mozilla.org.'in text_displayed, \
            'Message appears: " itisatrap.org has been reported as a deceptive site. You can report a detection ' \
            'problem or ignore the risk and go to this unsafe site." "Learn more about deceptive sites and phishing ' \
            'at www.antiphishing.org. Learn more about Firefox’s Phishing and Malware Protection at ' \
            'support.mozilla.org."'

        location_to_deselection = Location(Screen.SCREEN_WIDTH/2, Screen.SCREEN_HEIGHT/2)

        click(location_to_deselection)

        click(ignore_the_risk_link_pattern)

        itisatrap_page_loaded = exists(get_me_out_of_here_button_pattern, FirefoxSettings.SITE_LOAD_TIMEOUT)
        assert itisatrap_page_loaded, 'itisatrap.org page loaded and the button "Get me out of here!" in the banner ' \
                                      'at the top displayed'

        this_isnt_a_deceptive_site_button_hidden = exists(this_isnt_a_deceptive_site_button_pattern)
        assert this_isnt_a_deceptive_site_button_hidden is False, '"This isn\'t a Deceptive site" button is hidden'
