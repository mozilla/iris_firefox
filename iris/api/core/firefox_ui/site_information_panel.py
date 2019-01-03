# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.api.core.pattern import Pattern


class SiteInformationPanel(object):
    SITE_INFORMATION_PANEL_LABEL = Pattern('site_information_panel_label.png')
    DISABLE_BLOCKING_BUTTON = Pattern('disable_blocking_for_this_site_button.png')
    ENABLE_BLOCKING_BUTTON = Pattern('enable_blocking_for_this_site_button.png')