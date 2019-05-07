# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.api.core.pattern import Pattern


class AboutPreferences(object):
    PRIVACY_AND_SECURITY_BUTTON_SELECTED = Pattern('category_privacy_button_selected.png')
    PRIVACY_AND_SECURITY_BUTTON_NOT_SELECTED = Pattern('category_privacy_button_not_selected.png')
    BROWSE = Pattern('browse_option.png')
    ABOUT_PREFERENCE_SEARCH_PAGE_PATTERN = Pattern('about_preferences_search_page.png')
    DOWNLOADS = Pattern('downloads_about_preference.png')
    FIND_IN_OPTIONS = Pattern('find_in_options.png')

    class Privacy(object):
        CONTENT_TRACKING_TRACKERS_CHECKBOX_SELECTED = \
            Pattern('content_blocking_tracking_protection_checkbox_selected.png')
        CONTENT_TRACKING_TRACKERS_CHECKBOX_NOT_SELECTED = \
            Pattern('content_blocking_tracking_protection_checkbox_not_selected.png')
        CONTENT_TRACKING_TRACKERS_ALWAYS_RADIO_SELECTED = \
            Pattern('content_blocking_tracking_protection_option_always_radio_selected.png')
        CONTENT_TRACKING_TRACKERS_ALWAYS_RADIO_NOT_SELECTED \
            = Pattern('content_blocking_tracking_protection_option_always_radio_not_selected.png')
        CONTENT_TRACKING_TRACKERS_ONLY_PRIVATE_WINDOWS_RADIO_SELECTED = \
            Pattern('content_blocking_tracking_protection_option_private_radio_selected.png')
        CONTENT_TRACKING_TRACKERS_ONLY_PRIVATE_WINDOWS_RADIO_NOT_SELECTED = \
            Pattern('content_blocking_tracking_protection_option_private_radio_not_selected.png')

        TRACKING_PROTECTION_EXCEPTIONS_BUTTON = Pattern('tracking_protection_exceptions_button.png')

        class Exceptions(object):
            EXCEPTIONS_CONTENT_BLOCKING_LABEL = Pattern('exceptions_content_blocking_label.png')
            REMOVE_WEBSITE_BUTTON = Pattern('remove_website_permission_button.png')
            SAVE_CHANGES_BUTTON = Pattern('save_changes_btn_apply_changes_button.png')
