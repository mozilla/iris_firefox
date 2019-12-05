# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.


import logging

import bugzilla
from github import Github

from moziris.configuration.config_parser import get_config_property, validate_section
from moziris.api.os_helpers import OSHelper
from targets.firefox.errors import BugManagerError

logger = logging.getLogger(__name__)

bugzilla_os = {"win": "Windows 10", "win7": "Windows 7", "linux": "Linux", "osx": "macOS"}


def get_github_issue(bug_id):
    """Get Github issues details."""
    if len(validate_section("GitHub")) > 0:
        return None

    github_api_key = Github(get_config_property("GitHub", "github_key"))

    try:
        repo = [x for x in github_api_key.get_user().get_repos() if x.name == "iris2"]
        return repo[0].get_issue(bug_id)
    except Exception:
        return None


def get_bugzilla_bug(bug_id):
    """Get Bugzilla bug details."""
    if len(validate_section("Bugzilla")) > 0:
        return None

    bugzilla_api_key = get_config_property("Bugzilla", "api_key")
    base_url = get_config_property("Bugzilla", "bugzilla_url")

    try:
        b = bugzilla.Bugzilla(url=base_url, api_key=bugzilla_api_key)
        return b.get_bug(bug_id)
    except Exception:
        return None


def is_blocked(bug_id):
    """Checks if a Github issue/Bugzilla bug is blocked or not."""
    try:
        if "issue_" in bug_id:
            bug = get_github_issue(bug_id)
            if bug is None:
                return True
            if bug.state == "closed":
                return False
            else:
                if OSHelper.get_os() in bug.title:
                    return True
                return False
        else:
            bug = get_bugzilla_bug(bug_id)
            if bug is None:
                return True
            if bug.status in ["CLOSED", "RESOLVED"]:
                return False
            else:
                if bugzilla_os[OSHelper.get_os().value] == bug.op_sys or bug.platform in ["All", "Unspecified"]:
                    return True
                return False
    except BugManagerError as e:
        logger.error(str(e))
        return True
