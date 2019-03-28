# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = 'This is a test for opening the first default topsite from TOP SITES list by clicking on it'
        self.enabled = False

    def run(self):
        url = 'about:home'
        top_sites_pattern = Pattern('top_sites.png')
        youtube_top_site_pattern = Pattern('youtube_top_site.png')
        youtube_pattern = Pattern('youtube.png')

        navigate(url)

        expected_1 = exists(top_sites_pattern, 10)
        assert_true(self, expected_1, 'Find top sites image')

        click(youtube_top_site_pattern)
        expected_2 = exists(youtube_pattern, 10)
        assert_true(self, expected_2, 'Find youtube image')
