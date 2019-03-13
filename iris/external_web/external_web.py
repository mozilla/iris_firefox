# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


from iris.api.core.pattern import Pattern


class ExternalWeb(object):
    """CNN Site"""
    CNN_LOGO = Pattern('cnn_logo.png')
    CNN_BLOCKED_CONTENT_ADV = Pattern('cnn_blocked_content.png')
