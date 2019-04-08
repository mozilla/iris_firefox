# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from targets.firefox.firefox_ui.helpers.keyboard_shortcuts import *
from targets.firefox.firefox_ui.web_links.local_web import LocalWeb
from targets.firefox.firefox_app.fx_browser import Profiles, get_firefox_version
from targets.firefox.firefox_ui.bookmarks import Bookmarks
from targets.firefox.firefox_ui.helpers.update_rules import is_update_required, get_rule_for_channel, get_update_rules
from targets.firefox.firefox_ui.test_utils import restore_firefox_focus, open_clear_recent_history_window


from targets.firefox.test_assert import *