# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from moziris.api.finder.pattern import Pattern


class HamburgerMenu(object):

    ADDONS = Pattern("hamburger_menu_addons.png")
    SAVE_OPTIONS = Pattern("hamburger_menu_save_options.png")
    NEW_WINDOW = Pattern("hamburger_menu_new_window.png")
    HAMBURGER_MENU_ZOOM_INDICATOR = Pattern("appMenu_zoom_controls.png")
    EDIT_BUTTONS_BELOW_ZOOM_BUTTONS = Pattern("edit_buttons_below_zoom_buttons.png")
    HAMBUREGR_MENU = Pattern("panelui_menu_button.png")
    HAMBURGER_MENU_FIND_IN_PAGE_PATTERN = Pattern("hamburger_menu_find_in_page_pattern.png")

    RESTORE_PREVIOUS_SESSION = Pattern("restore_previous_session.png")
    CUSTOMIZE = Pattern("hamburger_customize.png")
    PRINT = Pattern("hamburger_print.png")
    WEB_DEVELOPER = Pattern("web_developer.png")
    HELP = Pattern("hamburger_help.png")
    EXIT = Pattern("hamburger_exit.png")