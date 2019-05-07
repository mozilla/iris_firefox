# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.api.core.pattern import Pattern


class AboutAddons(object):
    THEMES = Pattern('themes.png')

    class Themes(object):
        DARK_THEME = Pattern('dark_theme.png')
        LIGHT_THEME = Pattern('light_theme.png')
        DEFAULT_THEME = Pattern('default_theme.png')

        ENABLE_BUTTON = Pattern('enable_button.png')
        DISABLE_BUTTON = Pattern('disable_button.png')
        IRIS_TAB_LIGHT_OR_DEFAULT_THEME = Pattern('iris_tab_light_theme.png').similar(0.75)
        IRIS_TAB_DARK_THEME = Pattern('iris_tab_dark_theme.png').similar(0.75)
