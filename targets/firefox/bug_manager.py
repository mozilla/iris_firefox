# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this file,
# You can obtain one at http://mozilla.org/MPL/2.0/.

from github import Github
import bugzilla
from src.configuration.config_parser import get_config_property
from src.core.api.os_helpers import OSHelper
from src.core.api.errors import BugManagerError

api_key = get_config_property('Bugzilla', 'api_key')
base_url = get_config_property('Bugzilla', 'bugzilla_url')
g = Github(get_config_property('GitHub', 'github_key'))

bugzilla_os = {'win': 'Windows 10', 'win7': 'Windows 7', 'linux': 'Linux', 'mac': 'macOS'}


def get_github_issue(id):
    try:
        repo = [x for x in g.get_user().get_repos() if x.name == 'iris2']
        if len(repo) > 0:
            return repo[0].get_issue(id)
        else:
            return None
    except Exception:
        raise BugManagerError('Github API call failed')


def get_bugzilla_bug(id):
    try:
        b = bugzilla.Bugzilla(url=base_url, api_key=api_key)
        return b.get_bug(id)
    except Exception:
        raise BugManagerError('Bugzilla API call failed')


def is_blocked(id):
    try:
        if 'issue_' in id:
            bug = get_github_issue(id).state
            if bug.state == 'closed':
                return False
            else:
                if OSHelper.get_os() in bug.title:
                    return True
                else:
                    return False
        else:
            bug = get_bugzilla_bug(id)
            print(bug.status, bug.platform)
            if bug.status in ['CLOSED', 'RESOLVED']:
                return False
            else:
                if bugzilla_os[OSHelper.get_os()] == bug.platform or bug.platform in ['All', 'Unspecified']:
                    return True
                else:
                    return False
    except BugManagerError:
        return True
