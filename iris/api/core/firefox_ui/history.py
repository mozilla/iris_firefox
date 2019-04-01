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

            # Focused time ranges.
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

    class RecentlyClosedTabs(object):
        RECENTLY_CLOSED_TABS_TITLE = Pattern('recently_closed_tabs_label.png')
        RESTORE_ALL_TABS = Pattern('closed_tabs_restore_all_items.png')

    class RecentlyClosedWindows(object):
        RECENTLY_CLOSED_WINDOWS_TITLE = Pattern('recently_closed_windows_label.png')
        RESTORE_ALL_WINDOWS = Pattern('closed_windows_restore_all_items.png')

    class ForgetLast(object):
        FORGET_TIMEFRAME_TITLE = Pattern('panelui_panic_button_success_icon.png')

        LAST_FIVE_MINUTES = Pattern('panelui_panic_5min.png')
        LAST_TWO_HOURS = Pattern('panelui_panic_2hr.png')
        LAST_24_HOURS = Pattern('panelui_panic_day.png')

        # Selected items
        LAST_FIVE_MINUTES_SELECTED = Pattern('panelui_panic_5min_selected.png')
        LAST_TWO_HOURS_SELECTED = Pattern('panelui_panic_2hr_selected.png')
        LAST_24_HOURS_SELECTED = Pattern('panelui_panic_day_selected.png')

        FORGET_BUTTON = Pattern('panelui_panic_view_button.png')
        SUCCESS_FORGET_MSG = Pattern('panelui_panic_button_success_msg.png')
        CLOSE_FORGET_PANEL_BUTTON = Pattern('panelui_panic_success_close_button.png')
