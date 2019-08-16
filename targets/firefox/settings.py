# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


class FirefoxSettings:
    TINY_FIREFOX_TIMEOUT = 3
    SHORT_FIREFOX_TIMEOUT = 5
    FIREFOX_TIMEOUT = 10
    SITE_LOAD_TIMEOUT = 30
    HEAVY_SITE_LOAD_TIMEOUT = 90
    DEFAULT_FX_PREFS = {
        # Don't automatically update the application
        'app.update.disabledForTesting': True,
        # Don't restore the last open set of tabs if the browser has crashed
        'browser.sessionstore.resume_from_crash': False,
        # Don't check for the default web browser during startup
        'browser.shell.checkDefaultBrowser': False,
        # Don't warn on exit when multiple tabs are open
        'browser.tabs.warnOnClose': False,
        # Don't warn when exiting the browser
        'browser.warnOnQuit': False,
        # Don't send Firefox health reports to the production server
        'datareporting.healthreport.documentServerURI': 'http://%(server)s/healthreport/',
        # Skip data reporting policy notifications
        'datareporting.policy.dataSubmissionPolicyBypassNotification': False,
        # Only install add-ons from the profile and the application scope
        # Also ensure that those are not getting disabled.
        # see: https://developer.mozilla.org/en/Installing_extensions
        'extensions.enabledScopes': 5,
        'extensions.autoDisableScopes': 10,
        # Don't send the list of installed addons to AMO
        'extensions.getAddons.cache.enabled': False,
        # Don't install distribution add-ons from the app folder
        'extensions.installDistroAddons': False,
        # Don't automatically update add-ons
        'extensions.update.enabled': False,
        # Don't open a dialog to show available add-on updates
        'extensions.update.notifyUser': False,
        # Enable test mode to run multiple tests in parallel
        'focusmanager.testmode': True,
        # Enable test mode to not raise an OS level dialog for location sharing
        'geo.provider.testing': True,
        # Suppress delay for main action in popup notifications
        'security.notification_enable_delay': 0,
        # Suppress automatic safe mode after crashes
        'toolkit.startup.max_resumed_crashes': -1,
        # Don't send Telemetry reports to the production server. This is
        # needed as Telemetry sends pings also if FHR upload is enabled.
        'toolkit.telemetry.server': 'http://%(server)s/telemetry-dummy/',
    }
