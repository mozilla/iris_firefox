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
