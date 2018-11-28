# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.api.core.pattern import Pattern


class Sidebar(object):
    class SidebarHeader(object):
        SIDEBAR_ARROW_SWITCHER = Pattern('sidebar_switcher_arrow.png')
        SIDEBAR_CLOSE = Pattern('sidebar_close.png')

    class HistorySidebar(object):
        print
    class BookmarksSidebar(object):
        print
    class SyncedTabsSidebar(object):
        print

