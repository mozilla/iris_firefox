# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from pattern import Pattern
from util.parse_args import parse_args


class LocalWeb(object):
    """Constants that represent URLs and images for local content. """

    _ip_host = '127.0.0.1'
    _domain_host = 'localhost.allizom.org'
    _port = parse_args().port

    """Simple blank HTML page."""
    BLANK_PAGE = 'http://%s:%s/blank.htm' % (_ip_host, _port)
    BLANK_PAGE_2 = 'http://%s:%s/blank.htm' % (_domain_host, _port)

    """Local Firefox site."""
    FIREFOX_TEST_SITE = 'http://%s:%s/firefox/' % (_ip_host, _port)
    FIREFOX_TEST_SITE_2 = 'http://%s:%s/firefox/' % (_domain_host, _port)
    FIREFOX_LOGO = Pattern('firefox_logo.png')
    FIREFOX_IMAGE = Pattern('firefox_full.png')
    FIREFOX_BOOKMARK = Pattern('firefox_bookmark.png')
    FIREFOX_BOOKMARK_SMALL = Pattern('firefox_bookmark_small.png')

    """Local Firefox Focus site."""
    FOCUS_TEST_SITE = 'http://%s:%s/focus/' % (_ip_host, _port)
    FOCUS_TEST_SITE_2 = 'http://%s:%s/focus/' % (_domain_host, _port)
    FOCUS_LOGO = Pattern('focus_logo.png')
    FOCUS_IMAGE = Pattern('focus_full.png')
    FOCUS_BOOKMARK = Pattern('focus_bookmark.png')
    FOCUS_BOOKMARK_SMALL = Pattern('focus_bookmark_small.png')

    """Local Mozilla site."""
    MOZILLA_TEST_SITE = 'http://%s:%s/mozilla/' % (_ip_host, _port)
    MOZILLA_TEST_SITE_2 = 'http://%s:%s/mozilla/' % (_domain_host, _port)
    MOZILLA_LOGO = Pattern('mozilla_logo.png')
    MOZILLA_IMAGE = Pattern('mozilla_full.png')
    MOZILLA_BOOKMARK = Pattern('mozilla_bookmark.png')
    MOZILLA_BOOKMARK_SMALL = Pattern('mozilla_bookmark_small.png')

    """Local Pocket site."""
    POCKET_TEST_SITE = 'http://%s:%s/pocket/' % (_ip_host, _port)
    POCKET_TEST_SITE_2 = 'http://%s:%s/pocket/' % (_domain_host, _port)
    POCKET_LOGO = Pattern('pocket_logo.png')
    POCKET_IMAGE = Pattern('pocket_full.png')
    POCKET_BOOKMARK = Pattern('pocket_bookmark.png')
    POCKET_BOOKMARK_SMALL = Pattern('pocket_bookmark_small.png')
