# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from targets.firefox.fx_testcase import *


class Test(FirefoxTest):
    fx_values = pytest.mark.VALUES(
        channel='beta',
        # exclude='osx',
        # profile='new',
        # fx_version="63",
        test_case_id="119484",
        test_suite_id="1902",
    )

    details = pytest.mark.DETAILS(
        description="This is a test experiment for text search ",
        locale='[en-US]',
        values=fx_values
    )
    @details
    def test_run(self):
        region = Region(0, 40, 200, 100)
        result=region.exists('Search a very')

        assert result ,"Assert_message for text search test "
