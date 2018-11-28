# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.api.core.pattern import Pattern


class History(object):



    class HistoryMenu(object):
        VIEW_HISTORY_SIDEBAR = Pattern('view_history_sidebar.png')
        CLEAR_RECENT_HISTORY = Pattern('clear_recent_history.png')
        RECENTLY_CLOSED_TABS = Pattern('recently_closed_tabs.png')
        RECENTLY_CLOSED_WINDOWS = Pattern('recently_closed_windows.png')
        SHOW_ALL_HISTORY = Pattern('show_all_history.png')

    class CLearRecentHistory(object):

        CLEAR_ALL_HISTORY_TITLE = Pattern('sanitize_dialog_title.png')
        CLEAR_RECENT_HISTORY_TITLE = Pattern('sanitize_dialog_non_everything_title.png')

        class TimeRange(object):
            LAST_HOUR = Pattern('last_hour.png')
            LAST_TWO_HOURS = Pattern('last_two_hours.png')
            LAST_FOUR_HOURS = Pattern('last_four_hours.png')
            TODAY = Pattern('today.png')
            EVERYTHING = Pattern('everything.png')
            CLEAR_CHOICE_LAST_HOUR = Pattern('sanitize_duration_choice_last_hour.png')
            CLEAR_CHOICE_LAST_TWO_HOURS = Pattern('sanitize_duration_choice_last_two_hours.png')
            CLEAR_CHOICE_LAST_FOUR_HOURS = Pattern('sanitize_duration_choice_last_four_hours.png')
            CLEAR_CHOICE_TODAY = Pattern('sanitize_duration_choice_today.png')
            CLEAR_CHOICE_EVERYTHING = Pattern('sanitize_duration_choice_everything.png')


        # History group.
        BROWSING_AND_DOWNLOAD_HISTORY = Pattern('browsing_and_download_history.png')
        COOKIES = Pattern('cookies.png')
        ACTIVE_LOGINS = Pattern('active_logins.png')
        CACHE = Pattern('cache.png')
        FORM_AND_SEARCH_HISTORY = Pattern('form_and_search_history.png')

        # Data group.
        SITE_PREFERENCES = Pattern('site_preferences.png')
        OFFLINE_WEBSITE_DATA = Pattern('offline_website_data.png')

        # Control buttons.
        CANCEL = Pattern('cancel_button.png')
        CLEAR_NOW = Pattern('clear_now_button.png')
        DISABLED_CLEAR_NOW = Pattern('disabled_clear_now_button.png')