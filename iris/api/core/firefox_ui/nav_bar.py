# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from iris.api.core.pattern import Pattern


class NavBar(object):
    BACK_BUTTON = Pattern('back_button.png')
    BACK_BUTTON_RTL = Pattern('back_button_rtl.png')
    FORWARD_BUTTON = Pattern('forward_button.png')
    FORWARD_BUTTON_RTL = Pattern('forward_button_rtl.png')
    RELOAD_BUTTON = Pattern('reload_button.png')
    RELOAD_BUTTON_RTL = Pattern('reload_button_rtl.png')
    HOME_BUTTON = Pattern('home_button.png')

    LIBRARY_MENU = Pattern('library_button.png')
    SIDEBAR_MENU = Pattern('sidebar_button.png')
    SIDEBAR_MENU_RTL = Pattern('sidebar_button_rtl.png')
    HAMBURGER_MENU = Pattern('panel_ui_menu_button.png')
    HAMBURGER_MENU_DARK_THEME = Pattern('panel_ui_menu_button_dark_theme.png')
    MORE_TOOLS = Pattern('more_tools.png')

    # Zoom navigation buttons are reachable on NavBar after drag and drop correspondent item from 'Customize...'
    # hamburger menu.
    ZOOM_RESET_BUTTON = Pattern('zoom_reset_button_100.png')
    ZOOM_RESET_BUTTON_90 = Pattern('zoom_reset_button_90.png')
    ZOOM_RESET_BUTTON_110 = Pattern('zoom_reset_button_110.png')
    ZOOM_OUT = Pattern('zoom_out_button.png')
    ZOOM_IN = Pattern('zoom_in_button.png')

    DEFAULT_ZOOM_LEVEL_TOOLBAR_CUSTOMIZE_PAGE = Pattern('default_zoom_level_toolbar_customize_page.png')
    ZOOM_CONTROLS_CUSTOMIZE_PAGE = Pattern('wrapper_zoom_controls.png')
    TOOLBAR = Pattern('toolbar.png')

    DOWNLOADS_BUTTON = Pattern('downloads_button.png')
    DOWNLOADS_BUTTON_BLUE = Pattern('downloads_button_blue.png').similar(0.95)
    DOWNLOADS_BUTTON_GREY = Pattern('downloads_button_grey.png').similar(0.95)
    SEVERE_DOWNLOADS_BUTTON = Pattern('downloads_button_severe.png')
    UNWANTED_DOWNLOADS_BUTTON = Pattern('downloads_button_warning.png')
    CUSTOM_DOWNLOADS_BUTTON = Pattern('custom_downloads_button.png')
    CUSTOM_DOWNLOADS_BUTTON_BLUE = Pattern('custom_downloads_button_blue.png')
    BAR = Pattern('new_place.png')

    class ContextMenu(object):
        BOOKMARKS_TOOLBAR = Pattern('navbar_context_menu_bookmarks_toolbar.png')
