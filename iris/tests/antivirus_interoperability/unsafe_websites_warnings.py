# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.test_case import *


class Test(BaseTest):

    def __init__(self):
        BaseTest.__init__(self)
        self.meta = "Warnings are displayed if unsafe websites are accessed or downloads initiated."
        self.test_case_id = "219583"
        self.test_suite_id = "3036"
        self.locale = ["en-US"]

    def run(self):
        soap_wiki_footer_pattern = Pattern('soap_wiki_footer.png')