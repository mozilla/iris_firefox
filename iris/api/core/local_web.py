# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from util.parse_args import parse_args


class LocalWeb(object):
    """
    Constants that represent URLs and images for local content.
    """

    # Simple blank HTML page
    BLANK_PAGE = 'http://127.0.0.1:%s/blank.htm' % parse_args().port

    # Local Firefox site
    FIREFOX_TEST_SITE = 'http://127.0.0.1:%s/firefox/' % parse_args().port
    FIREFOX_LOGO = 'firefox_logo.png'
    FIREFOX_IMAGE = 'firefox_full.png'
    FIREFOX_BOOKMARK = 'firefox_bookmark.png'
    FIREFOX_BOOKMARK_SMALL = 'firefox_bookmark_small.png'

    # Local Firefox Focus site
    FOCUS_TEST_SITE = 'http://127.0.0.1:%s/focus/' % parse_args().port
    FOCUS_LOGO = 'focus_logo.png'
    FOCUS_IMAGE = 'focus_full.png'
    FOCUS_BOOKMARK = 'focus_bookmark.png'
    FOCUS_BOOKMARK_SMALL = 'focus_bookmark_small.png'

    # Local Mozilla site
    MOZILLA_TEST_SITE = 'http://127.0.0.1:%s/mozilla/' % parse_args().port
    MOZILLA_LOGO = 'mozilla_logo.png'
    MOZILLA_IMAGE = 'mozilla_full.png'
    MOZILLA_BOOKMARK = 'mozilla_bookmark.png'
    MOZILLA_BOOKMARK_SMALL = 'mozilla_bookmark_small.png'

    # Local Pocket site
    POCKET_TEST_SITE = 'http://127.0.0.1:%s/pocket/' % parse_args().port
    POCKET_LOGO = 'pocket_logo.png'
    POCKET_IMAGE = 'pocket_full.png'
    POCKET_BOOKMARK = 'pocket_bookmark.png'
    POCKET_BOOKMARK_SMALL = 'pocket_bookmark_small.png'

