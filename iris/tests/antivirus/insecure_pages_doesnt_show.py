from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'Check browser doesn\'t show insecure webpage erros'
        self.test_case_id = '225143'
        self.test_suite_id = '3063'
        self.locale = ['en-US']

    def run(self):
        insecure_connection_pattern = Pattern('https_insecure_sign.png')
        twitter_logo_pattern = Pattern('twitter_logo.png')
        tracker_site_pattern = Pattern('firefox_tracker_site_logo.png')

        change_preference('security.enterprise_roots.enabled', 'false')

        navigate('https://www.twitter.com')
        close_content_blocking_pop_up()
        twitter_page_loaded = exists(twitter_logo_pattern)
        assert_true(self, twitter_page_loaded, 'Twitter webpage is loaded successfully')

        connection_insecure_not_displayed_twitter = not exists(insecure_connection_pattern)
        assert_true(self, connection_insecure_not_displayed_twitter,
                    'No error stating that the "connection is not secured" is displayed for twitter page')

        navigate('https://itisatrap.org/firefox/its-a-tracker.html')
        close_content_blocking_pop_up()
        tracker_site_loaded = exists(tracker_site_pattern)
        assert_true(self, tracker_site_loaded, '"It\'s a tracker" site loaded')

        connection_insecure_not_displayed_tracker_site = not exists(insecure_connection_pattern)
        assert_true(self, connection_insecure_not_displayed_tracker_site,
                    'No error stating that the "connection is not secured" is displayed for default tracker site')
