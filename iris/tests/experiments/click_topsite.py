# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from test_case import *


class test(base_test):

    def __init__(self, app):
        base_test.__init__(self, app)
        self.meta = "This is a test for opening the first default topsite from TOP SITES list by clicking on it"

    def run(self):

        url = "about:home"
        top_sites_image = "top_sites.png"
        youtube_top_site_image = "youtube_top_site.png"
        youtube_image = "youtube.png"

        navigate(url)

        expected_1 = exists(top_sites_image, 0.5)
        assert_true(self, expected_1, 'Find top sites image')

        click(youtube_top_site_image)
        expected_2 = exists(youtube_image, 0.5)
        assert_true(self, expected_2, 'Find youtube image')
