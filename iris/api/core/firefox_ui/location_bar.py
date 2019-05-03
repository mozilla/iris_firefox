# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.api.core.pattern import Pattern


class LocationBar(object):
    IDENTITY_ICON = Pattern('identity_icon.png')
    INSECURE_CONNECTION_LOCK_DARK_THEME = Pattern('insecure_connection_lock_dark_theme.png')

    HISTORY_DROPMARKER = Pattern('history_dropmarker.png')
    PAGE_ACTION_BUTTON = Pattern('page_action_button.png')
    POCKET_BUTTON = Pattern('pocket_button.png')
    STAR_BUTTON_UNSTARRED = Pattern('star_button_unstarred.png')
    STAR_BUTTON_STARRED = Pattern('star_button_starred.png')

    URLBAR_ZOOM_BUTTON_30 = Pattern('urlbar_zoom_button_30.png')
    URLBAR_ZOOM_BUTTON_90 = Pattern('urlbar_zoom_button_90.png').similar(0.7)
    URLBAR_ZOOM_BUTTON_110 = Pattern('urlbar_zoom_button_110.png')
    URLBAR_ZOOM_BUTTON_300 = Pattern('urlbar_zoom_button_300.png')

    SEARCH_BAR = Pattern('search_bar.png')
    URL_BAR_DEFAULT_ZOOM_LEVEL = Pattern('url_bar_default_zoom_level.png')

    TRACKING_PROTECTION_SHIELD_ACTIVATED = Pattern('tracking_protection_icon_enabled.png')
    TRACKING_PROTECTION_SHIELD_DEACTIVATED = Pattern('tracking_protection_icon_disabled.png')
    NEW_FIREFOX_CONTENT_BLOCKING_LABEL = Pattern('uitour_tooltip_title_new_in_firefox_content_blocking.png')
    NEXT_BUTTON_TOUR_FIRST_STEP = Pattern('uitour_tooltip_next_button.png')
    TRACKING_ATTEMPTS_BLOCKED_MESSAGE = Pattern('tracking_attempts_blocked_message.png')
    TRACKING_CONTENT_DETECTED_MESSAGE = Pattern('tracking_content_detected_message.png')

    NEW_FIREFOX_CONTENT_BLOCKING_LABEL = Pattern('uitour_tooltip_title_new_in_firefox_content_blocking.png')
    NEXT_BUTTON_TOUR_FIRST_STEP = Pattern('uitour_tooltip_next_button.png')
